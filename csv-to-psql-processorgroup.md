### **🔹 NiFi Processor Group Plan**  
You need a **Processor Group** that:  
1. **Fetches a CSV** via HTTP (`InvokeHTTP`).  
2. **Splits CSV into rows** (`SplitRecord`).  
3. **Converts each row to a single string** (`ConvertRecord`).  
4. **Merges all rows into a bulk query** (`MergeRecord`).  
5. **Upserts into PostgreSQL** (`PutDatabaseRecord`).  
6. **Logs and prints data at every step** (`LogAttribute` → `PutFile`).  

---

### **🔹 Step-by-Step NiFi Flow**
#### **1️⃣ Fetch CSV from HTTP**  
**`InvokeHTTP`**  
- **Method:** `GET`  
- **Response Format:** CSV  
- **Success Relationship → `ConvertRecord`**  

**🔍 Debugging** → Connect **Success** to `LogAttribute` → `PutFile`  

---

#### **2️⃣ Convert CSV Rows to Strings**  
**`ConvertRecord`**  
- **Record Reader:** `CSVReader`  
- **Record Writer:** `FreeFormTextRecordSetWriter`  
- **Schema**: Converts all columns into **one string per row**  
  ```json
  {
    "type": "record",
    "name": "row",
    "fields": [
      { "name": "content", "type": "string" }
    ]
  }
  ```
- **Output Format:** `content="column1_value,column2_value,..."`

**🔍 Debugging** → Connect to `LogAttribute` → `PutFile`

---

#### **3️⃣ Merge All Rows into a Bulk Query**  
**`MergeRecord`**  
- **Merge Strategy:** `Defragment`  
- **Max Bin Age:** `1 sec` (forces batching quickly)  
- **Min Records:** `100` (adjust for performance)  
- **Record Reader:** `CSVReader`  
- **Record Writer:** `JSONRecordSetWriter`  

**🔍 Debugging** → Connect `MergeRecord` → `LogAttribute` → `PutFile`  

---

#### **4️⃣ Upsert Data into PostgreSQL**  
**`PutDatabaseRecord`**  
- **Database Type:** PostgreSQL  
- **Statement Type:** `Upsert` (Insert with conflict handling)  
- **Record Reader:** `JsonTreeReader`  
- **Table Name:** `your_table_name`  
- **On Conflict:** Set `PRIMARY KEY` in PostgreSQL to allow upsert behavior  
  ```sql
  CREATE TABLE your_table (
      id SERIAL PRIMARY KEY,
      content TEXT,
      created_at TIMESTAMP DEFAULT NOW()
  );
  ```

**🔍 Debugging** → Connect `PutDatabaseRecord` to `LogAttribute` → `PutFile`

---

### **🔹 Debugging & Logging Every Step**
1. **After `InvokeHTTP` → `PutFile`** (see raw CSV)  
2. **After `ConvertRecord` → `PutFile`** (see row strings)  
3. **After `MergeRecord` → `PutFile`** (see bulk JSON)  
4. **After `PutDatabaseRecord` → `PutFile`** (log errors or success messages)  

---

### **🚀 Next Steps**
1. Set up the **full flow** and check **PutFile outputs**.  
2. If errors occur, check **Data Provenance** and `LogAttribute` logs.  
3. Adjust schema and SQL query if **data isn't inserted correctly**.  

Would you like an example `.yaml` for `docker-compose` with PostgreSQL to test this? 🚀


Yes, using multiple **PutFile** processors—one for each step—is the best approach.  

### **🔹 Why?**
1. **Prevents Overwriting:** Each processor logs its own output separately.  
2. **Easier Debugging:** You can check each step's output individually.  
3. **Avoids Race Conditions:** Multiple processors writing to the same file can cause corruption or missing data.  

### **🔹 Recommended Setup**
| Processor         | PutFile Filename Example  |
|------------------|-------------------------|
| `InvokeHTTP`      | `/logs/invoke_http.csv`  |
| `ConvertRecord`   | `/logs/converted.txt`    |
| `MergeRecord`     | `/logs/merged.json`      |
| `PutDatabaseRecord` | `/logs/db_insert.log`   |

Each **PutFile** processor should have a **different filename**, or if you prefer, include timestamps to make each file unique:
```
/logs/${processor.name}_${now():format('yyyyMMddHHmmss')}.log
```

<h2 style="color:yellow">Formatting the output record of a processor</h2>

In our case, we don't know the number of columns we want to join into one string so we need to define the schema of our reader so it would treat each row as a map of columns (on the input side).
Therefore, we'll define the schema of our csv reader to treat the input as a map of strings:

### **Breaking Down the Schema**

#### **Schema Structure**
Your schema:
```json
{
  "type": "record",
  "name": "row",
  "fields": [
    { "name": "attributes", "type": { "type": "map", "values": ["null", "string"] } }
  ]
}
```
**Explanation:**
- **`type: "record"`** → This defines an **Avro record**, meaning the data is structured as key-value fields.
- **`name: "row"`** → This is the name of the record type (not a database table, just an identifier).
- **`fields`** → A list of named attributes in the record.

#### **What’s Inside `fields`?**
- **`name: "attributes"`** → This defines a single field in the record called `attributes`.
- **`type: { "type": "map", "values": ["null", "string"] }`**:
  - **`type: "map"`** → This means that `attributes` is a dynamic key-value structure.
  - **`values: ["null", "string"]`** → The values in the map can either be `null` or `string`.

  <h3 style="color:red">The schema is an Avro schema so the type is one of two options: JSON string naming a defined type or a JSON object of the form {type: "name" ...attributes...}</h3>

---

### **How This Schema Works in NiFi**
#### **Example Input CSV (from `InvokeHTTP`)**
```
"attribute1:name","attribute1:price","attribute2:name","attribute2:price"
"nameA1","priceA1",,
"nameB1","priceB1","nameB2","priceB2"
```

#### **How NiFi Interprets It Using This Schema**
Each **row** in the CSV will be transformed into a **record** with a **map**:
```json
{
  "attributes": {
    "attribute1:name": "nameA1",
    "attribute1:price": "priceA1",
    "attribute2:name": null,
    "attribute2:price": null
  }
}
```
```json
{
  "attributes": {
    "attribute1:name": "nameB1",
    "attribute1:price": "priceB1",
    "attribute2:name": "nameB2",
    "attribute2:price": "priceB2"
  }
}
```
- Each column name (`attribute1:name`, `attribute1:price`, etc.) becomes a **key** inside the `attributes` map.
- Each **row** is turned into a single record with **all the column values stored dynamically** inside the map.

---

### **Why Use a `map` Instead of Listing All Columns?**
- If you don’t know how many columns there are **ahead of time**, defining a fixed schema is impossible.
- A **map** allows NiFi to **automatically capture** any number of columns without needing to predefine them.

---

### **What Happens in `convertRecord`?**
- **Before `convertRecord`** → The data is still in CSV format.
- **After `convertRecord`** → Each row becomes a structured record with a dynamic map.

---

The output of the **CSVReader** will be a **record-based representation** of the CSV data, structured according to the **Avro schema** you define.

It's not JSON yet—it's still an **internal record format** that NiFi can process efficiently.

Once the data reaches **ConvertRecord** and is written using **FreeFormTextRecordSetWriter**, it will be converted into a **flattened string** based on your writer configuration.

<h2 style="color:yellow">Flattening the record's attributes field into a single string</h2>

Since the freeFormTextWriter allows only very simple string manipulation,
we need to add add an executeScript processor between convertRecord and 
mergeRecord that would take the text output from the freeFormTextWriter 
in convertRecord, somehow know it's a map (dict in Python),
join all keys and values and then send it back into the executeScript 
processor.

1. **ConvertRecord**:  
   - Uses **CSVReader** (with Avro schema) to parse CSV rows into **records**.
   - Uses **FreeFormTextRecordSetWriter** to **serialize** the records into text format.
   - The output is a **string**, but currently, it only contains the first column instead of all key-value pairs.

2. **ExecuteScript (Python)**:  
   - Reads the text output (which should represent a map/dictionary).
   - Parses the data, joining **all keys and values** into a single string.
   - Writes the transformed data back into the FlowFile.
   - Sends the updated FlowFile to **MergeRecord**.

3. **MergeRecord**:  
   - Receives the modified FlowFiles from **ExecuteScript**.
   - Merges multiple records together before inserting them into the database.

---

### 🔹 How to Implement `ExecuteScript`
Here’s a Python script that reads the FlowFile content, joins all key-value pairs, and rewrites it:

#### **Steps to Set Up ExecuteScript**
1. Add an **ExecuteScript** processor between **ConvertRecord** and **MergeRecord**.
2. In the **Script Engine** property, select **Python** (Jython).
3. Paste the following script into the **Script Body**:

```python
from org.apache.nifi.processor.io import InputStreamCallback, OutputStreamCallback
from org.apache.nifi.flowfile import FlowFile
from org.apache.nifi.processor import ProcessSession
from org.apache.commons.io import IOUtils
import json

# Type Annotations
session: ProcessSession  # Provided by NiFi implicitly
flowFile: FlowFile | None = session.get()  # FlowFile represents a NiFi data object

if flowFile is not None:
    try:
        # Read the FlowFile content
        class ReaderCallback(InputStreamCallback):
            def __init__(self):
                self.content: str = ""

            def process(self, inputStream):
                self.content = IOUtils.toString(inputStream, "UTF-8")

        reader = ReaderCallback()
        session.read(flowFile, reader)
        content: str = reader.content  # Read content as a string

        # Parse content as JSON
        data: dict[str, str | None] = json.loads(content)  # Dictionary of column_name -> value

        # Flatten the map into a single string: "key1=value1, key2=value2, ..."
        flattened: str = ", ".join(f"{k}={v}" for k, v in data.items() if v is not None)

        # Write the modified content back to the FlowFile
        class WriterCallback(OutputStreamCallback):
            def __init__(self, content: str):
                self.content = content

            def process(self, outputStream):
                outputStream.write(self.content.encode("UTF-8"))

        flowFile = session.write(flowFile, WriterCallback(flattened))

        # Transfer to success
        session.transfer(flowFile, REL_SUCCESS)

    except Exception as e:
        log.error("Error processing FlowFile", e)
        session.transfer(flowFile, REL_FAILURE)
```

---

### 🔹 Explanation of the Script:
- **Reads** the FlowFile content (expects it to be JSON from `FreeFormTextWriter`).
- **Parses** the JSON into a Python dictionary.
- **Joins** all key-value pairs into a **single string** like `"column1=value1, column2=value2"`.
- **Writes** the new string **back into the FlowFile**.
- **Transfers** it to `success`, or `failure` if an error occurs.

---

### 🔹 What You'll Get:
After this, the output will be a **single string** per row, like:

```
attribute1_name=nameA1, attribute1_price=priceA1, attribute2_name=nameB1, attribute2_price=priceB1
attribute1_name=nameA2, attribute1_price=priceA2, attribute2_name=nameB2, attribute2_price=priceB2
...
```

This ensures **MergeRecord** will get the properly formatted data.

---


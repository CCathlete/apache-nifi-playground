import org.apache.nifi.processor.io.StreamCallback;
import org.apache.nifi.flowfile.flowfile;
import org.apache.nifi.processor.ProcessSession;
import groovy.json.JsonSlurper;
import groovy.transform.CompileStatic;
import java.nio.charset.StandardCharsets;
import java.io.InputStreamReader;
import java.io.BufferedReader;

/**
* A custom processor body that goes into the executeScript processor.
* This processor reads the FlowFile content as input stream, joins
* all key-value pairs into a single string (it expects a map),
* and sends it back to the parent processor as output stream.
* The parent processor (executeScript) will then write it to the 
* FlowFile.
*/
@CompileStatic // Enforces static typing.
class FlattenAttributeProcessor implements StreamCallback
  void process(InputStream inputStream, OutputStream outputStream) throws IOException {
    BufferedReader reader = new BufferedReader(
      new InputStreamReader(inputStream, StandardCharsets.UTF_8)
    );
    String content = reader.text;
    Map<String, String> json = new JsonSlurper().parseText(content) as Map<String, Object>;

    Map<String, String> attributes = json.get("attributes") as Map<String, String>

    String Flattened = attributes.collect {String K, String V
    -> "$k=$v"
    }.join(", ")

    outputStream.write(flattened.getBytes(StandardCharsets.UTF_8))


    FlowFile flowFile = session.get()
    if (flowFile == null) return

    flowFile = session.write(flowFile, new FlattenAttributesProcessor())
    session.transfer(flowFile, REL_SUCCESS)

    }

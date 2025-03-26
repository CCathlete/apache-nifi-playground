# This is meant to go inside a NiFi processor which uses Jython.
# To be able to work with NiFi types, we need to import Java libraries.
from org.apache.nifi.processor.io import InputStreamCallback, OutputStreamCallback  # type: ignore
from org.apache.nifi.flowfile import FlowFile  # type: ignore
from org.apache.nifi.processor import ProcessSession  # type: ignore
from org.apache.commons.io import IOUtils  # type: ignore
from java.io import InputStream, OutputStream  # type: ignore
import json

# Log is a NiFi object passed implicitly by the executeScript
# processor.
# In case this script runs with Jython outside of the processor,
# we'll import and use the logging library instead.
try:
    log  # type: ignore
except NameError:
    import logging

    log = logging.getLogger(__name__)

if not REL_SUCCESS:  # type: ignore
    REL_SUCCESS: str = "success"


# Declarations

# Provided by NiFi implicitly
session: ProcessSession
# FlowFile represents a NiFi data object.
flowFile: FlowFile | None = session.get()

if flowFile is not None:  # Currently we're accepting flowFile = 0 or "" etc.
    try:
        # Reading the content of the FlowFile.
        class ReaderCallback(InputStreamCallback):
            def __init__(self) -> None:
                self.content: str = ""

            def process(
                self,
                inputStream: InputStream,
            ) -> None:

                self.content = IOUtils.toString(
                    inputStream,
                    "UTF-8",
                )

                reader = ReaderCallback()
                # Reading the content of the FlowFile into reader.content.
                session.read(flowFile, reader)
                content: str = reader.content

                # Treating the content (map) as JSON and serialising it into a dictionary.
                data: dict[str, str | None] = json.loads(content)

                # Flattening the map into a single string: "key1=value1, key2=value2, ..."
                flattened: str = ", ".join(
                    f"{column_name}={value}"
                    for column_name, value in data.items()
                    if value is not None
                )

                # Writing the modified content back to the FlowFile.
                class WriterCallback(OutputStreamCallback):
                    def __init__(
                        self,
                        content: str,
                    ) -> None:
                        self.content = content

                    def process(
                        self,
                        outputStream: OutputStream,
                    ) -> None:
                        outputStream.write(
                            self.content.encode("UTF-8"),
                        )

                        flowFile: FlowFile = session.write(
                            flowFile,
                            WriterCallback(flattened),
                        )

                        # Invoke success relationship.
                        session.transfer(
                            flowFile,
                            REL_SUCCESS,
                        )

    except Exception as e:
        log.error(f"Error processing FlowFile: {e}")

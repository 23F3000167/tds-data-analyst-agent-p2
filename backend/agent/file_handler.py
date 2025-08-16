import pandas as pd
import io

async def parse_files(files):
    summary = []
    parsed_data = {}

    for file in files:
        content = await file.read()
        name = file.filename
        summary.append(name)

        if name.endswith(".csv"):
            df = pd.read_csv(io.StringIO(content.decode("utf-8")))
            parsed_data[name] = df
        elif name.endswith(".json"):
            parsed_data[name] = content.decode("utf-8")
        # add support for .parquet, images, etc.

    return {"summary": summary, "parsed": parsed_data}

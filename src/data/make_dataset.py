# Imports
import pandas as pd
from glob import glob

# Import data


def load_from_files(files):
    accelerometer_data = pd.DataFrame()
    gyroscope_data = pd.DataFrame()
    acc_set = 1
    gyro_set = 1

    for f in files:
        splits = f.split("\\")[-1].split("_")[0].split("-")
        participant = splits[0]
        activity = splits[1]
        category = "".join(i for i in splits[2] if not i.isdigit())

        df = pd.read_csv(f)
        df["participant"] = participant
        df["activity"] = activity
        df["category"] = category
        if "Accelerometer" in f:
            df["set"] = acc_set
            accelerometer_data = pd.concat([accelerometer_data, df])
            acc_set += 1
        else:
            df["set"] = gyro_set
            gyroscope_data = pd.concat([gyroscope_data, df])
            gyro_set += 1
    accelerometer_data.index = pd.to_datetime(
        accelerometer_data["epoch (ms)"], unit="ms"
    )
    gyroscope_data.index = pd.to_datetime(gyroscope_data["epoch (ms)"], unit="ms")
    accelerometer_data.drop(
        columns=["time (01:00)", "epoch (ms)", "elapsed (s)"], inplace=True
    )
    gyroscope_data.drop(
        columns=["time (01:00)", "epoch (ms)", "elapsed (s)"], inplace=True
    )

    return accelerometer_data, gyroscope_data


# Load data from files
files = glob("../../data/raw/MetaMotion/MetaMotion/*.csv")


accel_df, gyro_df = load_from_files(files)

# merge datasets
df = pd.concat([accel_df.iloc[:, :3], gyro_df], axis=1)
df.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "participant",
    "activity",
    "category",
    "set",
]
sampling_func = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyro_x": "mean",
    "gyro_y": "mean",
    "gyro_z": "mean",
    "participant": "first",
    "activity": "first",
    "category": "first",
    "set": "first",
}
df[0:100].resample("200ms").apply(sampling_func)
# split the data by day
days = [g for n, g in df.groupby(pd.Grouper(freq="D"))]
df = pd.concat([g.resample("200ms").apply(sampling_func).dropna() for g in days])
df["set"] = df["set"].astype("int")
df.to_pickle("../../data/interim/01_data_processed.pkl")

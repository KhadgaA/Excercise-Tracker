import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.style.use("seaborn-v0_8-darkgrid")
mpl.rcParams["figure.figsize"] = (20, 5)
mpl.rcParams["figure.dpi"] = 200

df = pd.read_pickle("../../data/interim/01_data_processed.pkl")
# plotting all different activities

for activity in df["activity"].unique():
    # fig,ax = plt.subplots()
    activity_df = df[df["activity"] == activity][0:100]
    plt.plot(range(len(activity_df)), activity_df["acc_x"], label=activity)
plt.legend()
plt.show()
df


# Compare medium vs heavy excercise
category_df = df.query("activity == 'squat'").query("participant == 'B'").reset_index()
category_df.groupby("category")["acc_y"].plot(legend=True)

# Compare participants
participant_df = (
    df.query("activity == 'squat'").sort_values("participant").reset_index()
)
participant_df.groupby("participant")["acc_y"].plot(legend=True)

# Plot multiple axis

activities = df["activity"].unique()
participants = df["participant"].unique()
for activity in activities:
    for participant in participants:
        all_data = (
            df.query(f"activity == '{activity}'")
            .query(f"participant == '{participant}'")
            .reset_index()
        )

        if all_data.shape[0] > 0:
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

            fig.suptitle(f"{activity} - {participant}", fontsize=16)

            all_data[["acc_x", "acc_y", "acc_z"]].plot(
                sharex=True,
                ax=ax1,
                ylabel="Acceleration (g)",
                # title="Accelerometer data",
                legend=True,
                figsize=(20, 10),
            )
            ax1.legend(
                loc="upper center",
                shadow=True,
                fancybox=True,
                ncol=3,
                fontsize="x-large",
                bbox_to_anchor=(0.5, 1.15),
            )

            all_data[["gyro_x", "gyro_y", "gyro_z"]].plot(
                ylabel="Angular velocity (deg/s)",
                ax=ax2,
                xlabel="Samples",
                # title="Gyroscope data",
            )
            ax2.legend(
                loc="upper center",
                shadow=True,
                fancybox=True,
                ncol=3,
                fontsize="x-large",
                bbox_to_anchor=(0.5, 1.15),
            )
            plt.savefig(f"../../reports/figures/{activity}_{participant}.png")
            plt.tight_layout()
            plt.show()
plt.close("all")

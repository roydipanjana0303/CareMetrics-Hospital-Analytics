import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PURPLE = "#6C55E2"
BLUE = "#3B82F6"
NAVY = "#20243A"
GRID = "#E9EDF5"


def _prepare_ax(ax, title, xlabel, ylabel):
    ax.set_facecolor("white")
    ax.set_title(title, fontsize=12, fontweight="bold", color=NAVY, pad=12)
    ax.set_xlabel(xlabel, fontsize=9, color="#7B8496", labelpad=8)
    ax.set_ylabel(ylabel, fontsize=9, color="#7B8496", labelpad=8)
    ax.tick_params(colors="#7B8496", labelsize=8)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRID)


def plot_hospital_bar(df):
    """Bar Chart: Top 10 Hospitals by Patient Volume."""
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    fig.patch.set_facecolor("white")
    hospital_counts = df['Hospital_Name'].value_counts().head(10).reset_index()
    hospital_counts.columns = ['Hospital_Name', 'Count']

    sns.barplot(
        data=hospital_counts,
        x='Hospital_Name',
        y='Count',
        hue='Hospital_Name',
        palette=['#7C67E8'] * len(hospital_counts),
        legend=False,
        ax=ax,
        width=0.62,
    )
    _prepare_ax(ax, "Patient volume by hospital", "", "Patient count")
    ax.tick_params(axis="x", rotation=18)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    for container in ax.containers:
        ax.bar_label(container, padding=3, fontsize=8, color="#697187")
    plt.tight_layout()
    return fig


def plot_gender_pie(df):
    """Pie chart for the gender distribution of filtered patients."""
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    fig.patch.set_facecolor("white")
    if 'Gender' not in df.columns:
        ax.text(0.5, 0.5, 'Gender not available', ha='center', va='center')
        ax.set_axis_off()
        plt.tight_layout()
        return fig
    gender_counts = df['Gender'].fillna('Unknown').value_counts()

    ax.pie(
        gender_counts.values,
        labels=gender_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=["#6C55E2", "#EC7C86", "#4DA9DE"][:len(gender_counts)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 4},
        textprops={'fontsize': 8, 'color': '#697187'},
    )
    ax.set_title('Patient Gender Distribution', fontsize=12, fontweight='bold', color=NAVY, pad=12)
    ax.axis('equal')
    plt.tight_layout()
    return fig


def plot_admission_line(df):
    """Line chart for monthly patient admissions."""
    fig, ax = plt.subplots(figsize=(9.2, 3.8))
    fig.patch.set_facecolor("white")
    if 'Admission_Date' not in df.columns:
        ax.text(0.5, 0.5, 'Admission date not available', ha='center', va='center')
        ax.set_axis_off()
        plt.tight_layout()
        return fig
    dates = df['Admission_Date'].dropna()
    if len(dates) == 0:
        ax.text(0.5, 0.5, 'Admission date not available', ha='center', va='center')
        ax.set_axis_off()
        plt.tight_layout()
        return fig
    monthly_counts = dates.dt.to_period('M').value_counts().sort_index()
    monthly_counts.index = monthly_counts.index.astype(str)

    sns.lineplot(
        x=monthly_counts.index,
        y=monthly_counts.values,
        marker='o',
        color=PURPLE,
        linewidth=2.2,
        markersize=7,
        ax=ax
    )
    ax.fill_between(
        range(len(monthly_counts)),
        monthly_counts.values,
        color=PURPLE,
        alpha=0.08,
    )
    ax.set_xticks(range(len(monthly_counts)))
    ax.set_xticklabels(monthly_counts.index, rotation=35, ha='right')
    _prepare_ax(ax, "Monthly patient admissions", "Admission month", "Patient count")
    plt.tight_layout()
    return fig


def plot_age_histogram(df):
    """Histogram and KDE for the age distribution."""
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    fig.patch.set_facecolor("white")
    if 'Age' not in df.columns:
        ax.text(0.5, 0.5, 'Age not available', ha='center', va='center')
        ax.set_axis_off()
        plt.tight_layout()
        return fig
    ages = pd.to_numeric(df['Age'], errors='coerce').dropna()
    if len(ages) == 0:
        ax.text(0.5, 0.5, 'Age not available', ha='center', va='center')
        ax.set_axis_off()
        plt.tight_layout()
        return fig

    sns.histplot(
        ages,
        bins=12,
        kde=True,
        color=BLUE,
        edgecolor='white',
        linewidth=0.5,
        ax=ax,
    )
    _prepare_ax(ax, "Patient age distribution", "Age", "Patient count")
    plt.tight_layout()
    return fig


def plot_cost_boxplot(df):
    """Box plot of treatment cost across medical conditions."""
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    fig.patch.set_facecolor("white")
    if 'Treatment_Cost' not in df.columns or 'Medical_Condition' not in df.columns:
        ax.text(0.5, 0.5, 'Cost or condition not available', ha='center', va='center')
        ax.set_axis_off()
        plt.tight_layout()
        return fig

    sns.boxplot(
        data=df,
        x='Medical_Condition',
        y='Treatment_Cost',
        hue='Medical_Condition',
        palette=['#9B8AF5', '#69B3F2', '#F2A0A8', '#77C8B7', '#F2C879', '#8798B5'],
        legend=False,
        ax=ax
    )
    _prepare_ax(ax, "Treatment cost by condition", "", "Treatment cost (₹)")
    ax.tick_params(axis="x", rotation=22)
    plt.tight_layout()
    return fig
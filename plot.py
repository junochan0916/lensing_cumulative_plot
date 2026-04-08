import sys
import os
import numpy as np

import matplotlib
from matplotlib import rc
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica'], 'size': 20})
rc('text', usetex=True)
from matplotlib.transforms import blended_transform_factory
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'

import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# In production mode during a run, test should be set to False
test = False

# Reading data from this file, which contains a list of O4c events.
if not test:
    file_alerts = 'dataO4c.txt'
else:
    print('Test mode: should be disabled in production during O4c!!!')
    file_alerts = 'dataO4c_fake0.txt'

# -------------------------
# Event lists
# -------------------------
O1_gw_events  = [20150914, 20151012, 20151226]
O2_gw_events  = [20170104, 20170608, 20170729, 20170809, 20170814, 20170817, 20170818, 20170823]

O3a_gw_events = [20190403,20190408,20190412,20190413,20190413,20190421,20190425,20190426,
                 20190503,20190512,20190513,20190514,20190517,20190519,20190521,20190521,
                 20190527,20190602,20190620,20190630,20190701,20190706,20190707,20190708,
                 20190719,20190720,20190725,20190727,20190728,20190731,20190803,20190805,
                 20190814,20190828,20190828,20190910,20190915,20190916,20190917,20190924,
                 20190925,20190926,20190929,20190930]

O3b_gw_events = [20191103,20191105,20191109,20191113,20191126,20191127,20191129,20191204,
                 20191204,20191215,20191216,20191219,20191222,20191230,20200112,20200115,
                 20200128,20200129,20200202,20200208,20200208,20200209,20200210,20200216,
                 20200219,20200220,20200220,20200224,20200225,20200302,20200306,20200308,
                 20200311,20200316,20200322]

ER15_gw_events = [20230518]

O4a_gw_events = [20230529,20230531,20230601,20230603,20230605,20230606,20230606,20230608,
                 20230609,20230609,20230615,20230618,20230624,20230624,20230625,20230627,
                 20230628,20230630,20230630,20230702,20230702,20230704,20230704,20230706,
                 20230707,20230708,20230708,20230708,20230709,20230709,20230712,20230717,
                 20230721,20230723,20230723,20230726,20230728,20230729,20230731,20230803,
                 20230805,20230806,20230807,20230811,20230814,20230814,20230817,20230819,
                 20230820,20230822,20230823,20230824,20230824,20230825,20230830,20230831,
                 20230831,20230902,20230902,20230902,20230904,20230904,20230911,20230914,
                 20230919,20230920,20230920,20230922,20230922,20230924,20230925,20230927,
                 20230927,20230928,20230930,20231001,20231002,20231004,20231005,20231005,
                 20231005,20231008,20231013,20231014,20231018,20231020,20231026,20231028,
                 20231029,20231102,20231102,20231102,20231104,20231108,20231110,20231113,
                 20231113,20231113,20231114,20231118,20231118,20231118,20231119,20231120,
                 20231123,20231126,20231127,20231129,20231204,20231206,20231206,20231206,
                 20231213,20231220,20231221,20231223,20231223,20231223,20231224,20231226,
                 20231230,20231231,20231231,20240104,20240105,20240107,20240109]

O4b_gw_events = [20240413,20240421,20240422,20240426,20240426,20240428,20240430,20240501,
                 20240505,20240507,20240511,20240512,20240513,20240514,20240514,20240515,
                 20240520,20240525,20240527,20240527,20240530,20240531,20240601,20240601,
                 20240615,20240615,20240618,20240621,20240621,20240621,20240622,20240627,
                 20240629,20240630,20240703,20240705,20240716,20240807,20240813,20240813,
                 20240825,20240830,20240902,20240907,20240908,20240908,20240910,20240915,
                 20240915,20240916,20240917,20240919,20240920,20240920,20240921,20240922,
                 20240923,20240924,20240925,20240930,20240930,20241002,20241006,20241007,
                 20241009,20241009,20241009,20241011,20241101,20241102,20241102,20241109,
                 20241109,20241110,20241111,20241113,20241114,20241114,20241116,20241122,
                 20241125,20241127,20241129,20241130,20241130,20241201,20241210,20241210,
                 20241210,20241225,20241225,20241230,20241230,20241231,20250101,20250104,
                 20250108,20250109,20250109,20250114,20250118,20250118,20250118,20250119,
                 20250119]

previous_gw_events = (
    O1_gw_events + O2_gw_events + O3a_gw_events + O3b_gw_events + ER15_gw_events + O4a_gw_events + O4b_gw_events
)

# -------------------------
# Read O4c list from file
# -------------------------
O4c_list = []
try:
    with open(file_alerts, 'r') as f:
        for line in f:
            numeric_data = ''.join(filter(str.isdigit, line))
            numeric_data = '20' + numeric_data  # YYMMDD -> YYYYMMDD
            if numeric_data:
                O4c_list.append(int(numeric_data))
    O4c_list.sort()
except FileNotFoundError:
    print(f"can not find '{file_alerts}'")

gw_event = previous_gw_events + O4c_list
datetime_event = [datetime.strptime(str(event), '%Y%m%d') for event in gw_event]
num_event = len(datetime_event)

# -------------------------
# Run boundaries
# -------------------------
O1_start  = datetime(2015,  9, 12)
O1_end    = datetime(2016,  1, 19)
O2_start  = datetime(2016, 11, 30)
O2_end    = datetime(2017,  8, 25)
O3a_start = datetime(2019,  4,  1)
O3a_end   = datetime(2019, 10,  1)
O3b_start = datetime(2019, 11,  1)
O3b_end   = datetime(2020,  3, 27)

ER15_start = datetime(2023,  5, 15)
ER15_end   = datetime(2023,  5, 19)

O4a_start = datetime(2023,  5, 24)
O4a_end   = datetime(2024,  1, 16)

O4b_start = datetime(2024,  4, 10)
O4b_end   = datetime(2025,  1, 27)

O4c1_start = datetime(2025,  1, 28)
O4c1_end   = datetime(2025,  4,  1)
O4c2_start = datetime(2025,  6, 11)
O4c2_end   = datetime(2025, 11, 18)

# O5 expected period
O5_start   = datetime(2028,  1, 30)
O5_end     = datetime(2031,  2, 15)

# Lengths
len_O1   = (O1_end   - O1_start).days
len_O2   = (O2_end   - O2_start).days
len_O3a  = (O3a_end  - O3a_start).days
len_O3b  = (O3b_end  - O3b_start).days
len_ER15 = (ER15_end - ER15_start).days
len_O4a  = (O4a_end  - O4a_start).days
len_O4b  = (O4b_end  - O4b_start).days
len_O4c1 = (O4c1_end - O4c1_start).days
len_O4c2 = (O4c2_end - O4c2_start).days
len_O5   = (O5_end   - O5_start).days

print('len_O4c1=', len_O4c1, ', len_O4c2=', len_O4c2)

# Event counts
nev_O1   = len(O1_gw_events)
nev_O2   = len(O2_gw_events)
nev_O3a  = len(O3a_gw_events)
nev_O3b  = len(O3b_gw_events)
nev_ER15 = len(ER15_gw_events)
nev_O4a  = len(O4a_gw_events)
nev_O4b  = len(O4b_gw_events)

nev_O1_O3b  = nev_O1 + nev_O2 + nev_O3a + nev_O3b
nev_O1_ER15 = nev_O1_O3b + nev_ER15
nev_O1_O4a  = nev_O1_ER15 + nev_O4a
nev_O1_O4b  = nev_O1_O4a + nev_O4b
nev_O4c     = num_event - nev_O1_O4b

# O5 extrapolation
O5_rate_scale = 3.0
len_O4_total = len_ER15 + len_O4a + len_O4b + len_O4c1 + len_O4c2
nev_O4_total = nev_ER15 + nev_O4a + nev_O4b + nev_O4c
o4_rate_per_day = nev_O4_total / len_O4_total if len_O4_total > 0 else 0.0
o5_rate_per_day = O5_rate_scale * o4_rate_per_day
expected_O5_additional_events = o5_rate_per_day * len_O5
print('O5 expected rate = {:.3f} events/day ({:.1f}/yr), expected O5 events = {:.1f}'.format(
    o5_rate_per_day, o5_rate_per_day * 365.0, expected_O5_additional_events
))

# Days since O1 start
event_days = np.array([(d - O1_start).days for d in datetime_event], dtype=float)
cum = np.arange(1, num_event + 1)

# -------------------------
# Figure
# -------------------------
ratio_x = 10 * 0.618 * 1.2
ratio_y = 10 * 0.618
fig, ax = plt.subplots(dpi=100, figsize=(ratio_x, ratio_y))

# Today handling (your original logic)
date_today_utc_true = datetime.utcnow().date()
days_remaining = (O4c2_end.date() - date_today_utc_true).days
shift = 0 if days_remaining <= 3 else 3
date_today_utc = date_today_utc_true + timedelta(days=shift)

if test:
    date_today_utc = datetime(2025, 3, 10).date()

today      = datetime.strptime(str(date_today_utc),      '%Y-%m-%d')
today_true = datetime.strptime(str(date_today_utc_true), '%Y-%m-%d')

if today > O4c2_end:
    O4c = (O4c2_end - O1_start).days
elif today >= O4c2_start:
    O4c = (today - O1_start).days
elif today > O4c1_end:
    O4c = (today - O1_start).days
elif today >= O4c1_start:
    O4c = (today - O1_start).days
else:
    O4c = (today - O1_start).days

# Append the "today" endpoint for plotting stairs nicely
event_days = np.append(event_days, O4c)

# Run spans on x-axis
O1_start_day = 0
O1_end_day   = (O1_end   - O1_start).days
O2_start_day = (O2_start - O1_start).days
O2_end_day   = (O2_end   - O1_start).days
O3_start_day = (O3a_start - O1_start).days
O3_end_day   = (O3b_end   - O1_start).days
O4_start_day = (ER15_start - O1_start).days
O4b_start_day = (O4b_start - O1_start).days
O4c_total    = (O4c2_end  - O1_start).days
O5_start_day = (O5_start  - O1_start).days
O5_total     = (O5_end    - O1_start).days

x_axis_end_date = datetime(2030, 12, 31)
x_max_day = (x_axis_end_date - O1_start).days

ax.set_xlim(-80., x_max_day)
ax.set_yscale('log')
y_upper = max(1.05e3, 1.20 * (num_event + expected_O5_additional_events))
ax.set_ylim(1, y_upper)

# Background bands
run_spans = [
    ('O1', O1_start_day, O1_end_day),
    ('O2', O2_start_day, O2_end_day),
    ('O3', O3_start_day, O3_end_day),
    ('O4', O4_start_day, O4c_total),
    ('O5', O5_start_day, O5_total),
]
run_band_colors = ['#9fb7d9', '#c7c7c7', '#7fa0cf', '#a2a2a2', '#caa68f']
for i, (_, x_min, x_max) in enumerate(run_spans):
    ax.axvspan(x_min, x_max, color=run_band_colors[i], alpha=0.70, lw=0, zorder=0)

label_transform = blended_transform_factory(ax.transData, ax.transAxes)
for run_label, x_min, x_max in run_spans:
    if x_max <= x_min:
        continue
    ax.text(
        x_min + 0.5 * (x_max - x_min),
        1.015,
        run_label,
        transform=label_transform,
        ha='center',
        va='bottom',
        fontsize=16,
        fontweight='bold',
        color='0.15',
        clip_on=False,
    )

# Plot cumulative detections
color_curve = (0.2, 0.4, 0.65)
ax.stairs(cum, event_days, baseline=None, color=color_curve, linewidth=3)

# O5 expected extension
o5_x = np.array([O5_start_day, O5_total], dtype=float)
o5_y = np.array([num_event, num_event + expected_O5_additional_events], dtype=float)
ax.plot(
    o5_x, o5_y,
    linestyle='--',
    color='#8b1e3f',
    linewidth=2.8,
    label=r'O5 expected',
)

# Redraw O4b/c segment (as in your script)
cum_sub        = cum[nev_O1_O4a - 1:]
event_days_sub = event_days[nev_O1_O4a:]
event_days_sub = np.insert(event_days_sub, 0, O4b_start_day)
ax.stairs(cum_sub, event_days_sub, baseline=None, color=color_curve, linewidth=3)

# ------------------------------------------------------------
# Compute x_at_target for cum_target=1e3 (do NOT draw yet)
# ------------------------------------------------------------
cum_target = 1.0e3
x_at_target = None

# Use ONLY observed events for mapping cum -> x (exclude appended today point)
event_days_obs = np.asarray(event_days[:num_event], dtype=float)

if num_event >= cum_target:
    target_idx = int(cum_target) - 1
    x_at_target = float(event_days_obs[target_idx])
elif expected_O5_additional_events > 0 and (num_event + expected_O5_additional_events) >= cum_target:
    frac_to_target = (cum_target - num_event) / expected_O5_additional_events
    x_at_target = float(O5_start_day + frac_to_target * (O5_total - O5_start_day))

# Now marker
ax.plot(
    O4c, num_event,
    marker='o',
    markersize=9,
    markerfacecolor='white',
    markeredgecolor='k',
    markeredgewidth=2.0,
    linestyle='None',
    zorder=6,
)
ax.annotate(
    'Now',
    xy=(O4c, num_event),
    xytext=(8, 7),
    textcoords='offset points',
    fontsize=11,
    fontweight='bold',
    color='k',
)

ax.grid(False)
ax.set_ylabel('GW detections', fontsize=21, fontweight='bold', labelpad=12)
ax.set_xlabel('Year', fontsize=21, fontweight='bold', labelpad=13.5)

# X ticks (every 5 years)
tick_positions = []
tick_labels = []
plot_end_date = O1_start + timedelta(days=x_max_day)
for year in range(O1_start.year, plot_end_date.year + 1, 5):
    tick_date = datetime(year, 1, 1)
    if year == O1_start.year:
        tick_date = O1_start
    tick_day = (tick_date - O1_start).days
    if 0 <= tick_day <= x_max_day:
        tick_positions.append(tick_day)
        tick_labels.append(str(year))

tick_positions, tick_labels = zip(*sorted(zip(tick_positions, tick_labels)))
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, fontsize=15.5, fontweight='bold')

# Y ticks
yticks = [1, 10, 100, 1000]
ytick_labels = [r"$1$", r"$10$", r"$10^2$", r"$10^3$"]
ax.set_yticks(yticks)
ax.set_yticklabels(ytick_labels, fontsize=15.5, fontweight='bold')

# ------------------------------------------------------------
# Shade region above 10^3 (instead of drawing a horizontal line)
# ------------------------------------------------------------
ax.axhspan(
    1000,
    y_upper,
    facecolor='0.93',
    alpha=0.65,
    hatch='////',
    edgecolor='0.45',
    linewidth=0.0,
    zorder=1,
    label='_nolegend_',
)

# Place N_lens label inside the shaded region.
lens_label_y = 10 ** (0.5 * (np.log10(1000.0) + np.log10(y_upper)))
lens_label_transform = blended_transform_factory(ax.transAxes, ax.transData)
ax.text(
    0.82,
    lens_label_y,
    r'$\dot{N}_{\rm Lens} \sim 1/10^{3}$',
    transform=lens_label_transform,
    ha='center',
    va='center',
    fontsize=16,
    fontweight='bold',
    color='0.20',
    bbox=dict(facecolor='white', edgecolor='none', alpha=0.6, pad=1.5),
    zorder=7,
)

# Legend (unique entries)
handles, labels = ax.get_legend_handles_labels()
unique = {}
for h, lab in zip(handles, labels):
    if lab not in unique:
        unique[lab] = h

ax.legend(
    list(unique.values()),
    list(unique.keys()),
    loc='center right',
    #bbox_to_anchor=(0.52, 0.45),
    fontsize=16,
    frameon=False,
)

# Layout tweaks
plt.subplots_adjust(left=0.14, right=0.98, top=0.93, bottom=0.10)
ax.xaxis.set_label_coords(0.523, -0.060)

# Save
fnam = 'cumulative_events'
plt.savefig(fnam + '.pdf')
plt.savefig(fnam + '.png')
plt.close('all')

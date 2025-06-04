# ==================================================================
# V3
# Updated function

# 1. Save the current task list to a file (tasks.json)

# 2. Save the matrix plot as an image (eisenhower_matrix.png)

# 3. Load saved tasks on next startup

# Update v31, 

# Clear all tasks on each new app session

# Keep manual save/load available


# V32

# 1. Updated rating scale:
# Importance and Urgence now go from 1 to 5 instead of 0 to 4.

# 2. Prevent boundary placement:
# Adjusted plotted values by adding a small offset to keep points away from the edges.

# ==================================================================

# eisenhower_matrix.py
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import json

st.set_page_config(layout="wide")
st.title("📊 Eisenhower Matrix – Weekly Task Planner")


if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.tasks = []  # reset on new session
else:
    if "tasks" not in st.session_state:
        st.session_state.tasks = []


# File to store task data
TASK_FILE = "tasks.json"

# # Load saved tasks
# if "tasks" not in st.session_state:
#     if os.path.exists(TASK_FILE):
#         with open(TASK_FILE, "r") as f:
#             st.session_state.tasks = json.load(f)
#     else:
#         st.session_state.tasks = []

if st.button("🔄 Load Saved Tasks"):
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            st.session_state.tasks = json.load(f)
        st.success("Tasks loaded from file.")
    else:
        st.warning("No saved tasks found.")


# Save tasks to file
def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(st.session_state.tasks, f)

# -------------------- Input Form --------------------
with st.form("task_form"):
    name = st.text_input("Task Name")
    importance = st.slider("Importance", 1, 5)
    urgency = st.slider("Urgence", 1, 5)
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if name:
            st.session_state.tasks.append([name, importance, urgency])
            save_tasks()
        else:
            st.warning("Please enter a task name.")

# -------------------- Layout --------------------
col1, col2 = st.columns([2, 1])

# ---------- Eisenhower Matrix ----------
with col1:
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = {
        'Do': 'lightcoral',
        'Delegate': 'wheat',
        'Schedule': 'lightgreen',
        'Eliminate': 'lightgrey'
    }

    # Background zones
    ax.add_patch(patches.Rectangle((2.5, 2.5), 2.5, 2.5, color=colors['Do']))
    ax.add_patch(patches.Rectangle((0, 2.5), 2.5, 2.5, color=colors['Delegate']))
    ax.add_patch(patches.Rectangle((2.5, 0), 2.5, 2.5, color=colors['Schedule']))
    ax.add_patch(patches.Rectangle((0, 0), 2.5, 2.5, color=colors['Eliminate']))

    # Plot tasks
    for name, i, u in st.session_state.tasks:
        x = i - 0.2 if i >= 4.5 else i + 0.2
        y = u - 0.2 if u >= 4.5 else u + 0.2
        ax.scatter(x, y, c='blue', s=100, edgecolors='black')
        ax.text(x, y, name, fontsize=9, ha='center', va='center')

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xlabel("Importance")
    ax.set_ylabel("Urgence")
    ax.set_title("Eisenhower Matrix")
    ax.set_aspect('equal')
    ax.grid(True)

    # Labels
    ax.text(3.5, 4.8, 'Do', fontsize=10, ha='center', fontweight='bold')
    ax.text(1.5, 4.8, 'Delegate', fontsize=10, ha='center', fontweight='bold')
    ax.text(3.5, 0.2, 'Schedule', fontsize=10, ha='center', fontweight='bold')
    ax.text(1.5, 0.2, 'Eliminate', fontsize=10, ha='center', fontweight='bold')

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xticks(range(1, 5))
    ax.set_yticks(range(1, 5))
    
    # Add Arrow on both axies
    arrow_style = dict(arrowstyle='->', linewidth=2, mutation_scale=20)

    # X axis arrow
    ax.annotate('', xy=(5.0, 0), xytext=(0, 0), arrowprops=arrow_style)

    # Y axis arrow
    ax.annotate('', xy=(0, 5.0), xytext=(0, 0), arrowprops=arrow_style)



    # Save matrix image
    fig.savefig("eisenhower_matrix.png")

    # Show image download button
    with open("eisenhower_matrix.png", "rb") as f:
        st.download_button("📥 Download Matrix Image", f, file_name="eisenhower_matrix.png")

    st.pyplot(fig)

# ---------- Task List and Delete ----------
with col2:
    st.subheader("🗂 Task List")
    for i, task in enumerate(st.session_state.tasks):
        col_task, col_del = st.columns([4, 1])
        with col_task:
            st.markdown(f"- **{task[0]}** ({task[1]}, {task[2]})")
        with col_del:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                save_tasks()
                st.experimental_rerun()

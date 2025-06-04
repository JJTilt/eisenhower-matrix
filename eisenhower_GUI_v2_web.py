# eisenhower_matrix.py
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(layout="wide")
st.title("📊 Eisenhower Matrix – Weekly Task Planner")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Input form
with st.form("task_form"):
    name = st.text_input("Task Name")
    importance = st.slider("Importance", 0, 4)
    urgency = st.slider("Urgence", 0, 4)
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if name:
            st.session_state.tasks.append([name, importance, urgency])
        else:
            st.warning("Please enter a task name.")

# Layout: left = matrix, right = list
col1, col2 = st.columns([2, 1])

# ---------- MATRIX DISPLAY ----------
with col1:
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = {
        'Do': 'lightcoral',
        'Delegate': 'wheat',
        'Schedule': 'lightgreen',
        'Eliminate': 'lightgrey'
    }

    # Draw matrix background
    ax.add_patch(patches.Rectangle((2, 2), 2, 2, color=colors['Do']))
    ax.add_patch(patches.Rectangle((0, 2), 2, 2, color=colors['Delegate']))
    ax.add_patch(patches.Rectangle((2, 0), 2, 2, color=colors['Schedule']))
    ax.add_patch(patches.Rectangle((0, 0), 2, 2, color=colors['Eliminate']))

    # Plot tasks
    for name, i, u in st.session_state.tasks:
        ax.scatter(i, u, c='blue', s=100, edgecolors='black')
        ax.text(i, u, name, fontsize=9, ha='center', va='center')

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xlabel("Importance")
    ax.set_ylabel("Urgence")
    ax.set_title("Eisenhower Matrix")
    ax.set_aspect('equal')
    ax.grid(True)

    # Quadrant labels
    ax.text(3, 3.8, 'Do', fontsize=10, ha='center', fontweight='bold')
    ax.text(1, 3.8, 'Delegate', fontsize=10, ha='center', fontweight='bold')
    ax.text(3, 0.2, 'Schedule', fontsize=10, ha='center', fontweight='bold')
    ax.text(1, 0.2, 'Eliminate', fontsize=10, ha='center', fontweight='bold')

    st.pyplot(fig)

# ---------- TASK LIST + DELETE ----------
with col2:
    st.subheader("🗂 Task List")
    for i, task in enumerate(st.session_state.tasks):
        col_task, col_del = st.columns([4, 1])
        with col_task:
            st.markdown(f"- **{task[0]}** ({task[1]}, {task[2]})")
        with col_del:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                st.experimental_rerun()

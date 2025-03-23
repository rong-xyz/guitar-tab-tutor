import gradio as gr
import random
from explanation import get_guitar_explanation

def generate_question():
    """Generate a random music theory question."""
    keys = ["A", "B", "C", "D", "E", "F", "G"]
    major_minor = ["大调", "小调"]  # Major, Minor
    scale_degrees = list(range(1, 8))  # 1-7
    
    random_key = random.choice(keys)
    random_major_minor = random.choice(major_minor)
    random_degree = random.choice(scale_degrees)
    
    question = f"在{random_key}{random_major_minor}中的第{random_degree}级音阶是什么"
    
    return question, "无 (None)", None, "major (大调)", "", ""

def update_selection(accidental, note, chord_type):
    """Format the current selection for display."""
    if not note:
        return ""
    
    # Format the note with accidental
    note_part = note
    if accidental == "#":
        note_part = f"{note}<span style='font-size:inherit'>♯</span>"
    elif accidental == "♭":
        note_part = f"{note}<span style='font-size:inherit'>♭</span>"
    
    # Add chord type
    if chord_type == "minor (小调)":
        note_part += "<span style='font-size:inherit'>m</span>"
    elif chord_type == "diminished (减和弦)":
        note_part += "<span style='font-size:inherit'>°</span>"
    
    # Return as HTML with large font
    return f"<div style='font-size: 72px; text-align: center; font-weight: bold;'>{note_part}</div>"

def check_answer(accidental, note, chord_type, question, explanation_box):
    """Check if the answer is correct and provide guitar explanation."""
    if not note:
        return "请选择一个音符 (Please select a note)", explanation_box
    
    # Parse the question
    parts = question.split("在")[1].split("中的第")
    key_part = parts[0]
    degree_part = parts[1].split("级音阶是什么")[0]
    
    key = key_part[0]
    is_minor = "小调" in key_part
    degree = int(degree_part)
    
    # Define scales for all keys (major and minor)
    major_scales = {
        "C": ["C", "D", "E", "F", "G", "A", "B"],
        "D": ["D", "E", "F#", "G", "A", "B", "C#"],
        "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
        "F": ["F", "G", "A", "Bb", "C", "D", "E"],
        "G": ["G", "A", "B", "C", "D", "E", "F#"],
        "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
        "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"]
    }
    
    minor_scales = {
        "A": ["A", "B", "C", "D", "E", "F", "G"],
        "B": ["B", "C#", "D", "E", "F#", "G", "A"],
        "C": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
        "D": ["D", "E", "F", "G", "A", "Bb", "C"],
        "E": ["E", "F#", "G", "A", "B", "C", "D"],
        "F": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
        "G": ["G", "A", "Bb", "C", "D", "Eb", "F"]
    }
    
    # Get the correct answer
    if is_minor:
        correct_note = minor_scales[key][degree - 1]
    else:
        correct_note = major_scales[key][degree - 1]
    
    # Convert correct note for display
    correct_display = correct_note
    if "#" in correct_note:
        base_note = correct_note[0]
        correct_display = f"{base_note}♯"
    elif "b" in correct_note:
        base_note = correct_note[0]
        correct_display = f"{base_note}♭"
    
    # Format user answer
    user_answer = note
    if accidental and accidental != "无 (None)":
        user_answer += accidental
    
    # Check if user answer is correct
    normalized_correct = correct_note.replace("#", "♯").replace("b", "♭")
    normalized_user = user_answer
    
    is_correct = normalized_user == normalized_correct
    
    result_message = f"{'✓ 正确!' if is_correct else f'✗ 错误. 正确答案是 {correct_display}'}"
    
    # Get guitar explanation
    explanation = get_guitar_explanation(question, user_answer, normalized_correct)
    
    return result_message, explanation

# Define custom CSS
custom_css = """
    body {
        background-color: #121212;
        color: white;
    }
    .gradio-container {
        background-color: #121212;
    }
    .selection-container {
        display: flex;
        flex-direction: row;
        gap: 20px;
        margin-bottom: 20px;
    }
    .selection-column {
        flex: 1;
        padding: 10px;
        border: 1px solid #333;
        border-radius: 5px;
        background-color: #1e1e1e;
    }
    .note-display {
        text-align: center;
        font-size: 72px !important;
        margin: 20px 0;
        padding: 10px;
    }
    .note-display * {
        font-size: 72px !important;
    }
    .submit-btn {
        background-color: #e65c00 !important;
    }
    .radio-selected {
        background-color: #ffeb3b !important;
        color: black !important;
    }
    .explanation-box {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 5px;
        padding: 15px;
        margin-top: 20px;
    }
"""

# Create the interface with the custom theme
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 音乐理论测验 - Music Theory Quiz")
    
    with gr.Row():
        question_box = gr.Textbox(label="问题 (Question)", interactive=False)
        new_question_btn = gr.Button("生成新问题 (New Question)")
    
    gr.Markdown("### 选择你的答案 (Select your answer)")
    
    # Create 3 columns with selection options
    with gr.Row(elem_classes="selection-container"):
        with gr.Column(elem_classes="selection-column"):
            accidental_btn = gr.Radio(
                ["无 (None)", "#", "♭"], 
                label="变音记号 (Accidental)",
                value="无 (None)",
                interactive=True
            )
        
        with gr.Column(elem_classes="selection-column"):
            note_btn = gr.Radio(
                ["A", "B", "C", "D", "E", "F", "G"], 
                label="音符 (Note)",
                value=None,
                interactive=True
            )
        
        with gr.Column(elem_classes="selection-column"):
            chord_type_btn = gr.Radio(
                ["major (大调)", "minor (小调)", "diminished (减和弦)"],
                label="和弦类型 (Chord Type)",
                value="major (大调)",
                interactive=True
            )
    
    # Use HTML instead of Markdown for better display control
    current_selection = gr.HTML(
        value="",
        elem_classes="note-display",
        label=None
    )
    
    # Buttons for actions
    with gr.Row():
        clear_btn = gr.Button("清除选择 (Clear Selection)")
        submit_btn = gr.Button("确认答案 (Submit Answer)", elem_classes="submit-btn")
    
    # Result display
    result_box = gr.Textbox(label="结果 (Result)", interactive=False)
    
    # Guitar explanation box
    explanation_box = gr.Markdown(
        value="",
        label="吉他解释 (Guitar Explanation)",
        elem_classes="explanation-box"
    )
    
    # Set up event handlers
    new_question_btn.click(
        generate_question, 
        [], 
        [question_box, accidental_btn, note_btn, chord_type_btn, current_selection, explanation_box]
    )
    
    # Update selection display when any option changes
    accidental_btn.change(
        update_selection, 
        [accidental_btn, note_btn, chord_type_btn], 
        [current_selection]
    )
    
    note_btn.change(
        update_selection, 
        [accidental_btn, note_btn, chord_type_btn], 
        [current_selection]
    )
    
    chord_type_btn.change(
        update_selection, 
        [accidental_btn, note_btn, chord_type_btn], 
        [current_selection]
    )
    
    # Clear selection button
    clear_btn.click(
        lambda: ("无 (None)", None, "major (大调)", "", ""),
        [],
        [accidental_btn, note_btn, chord_type_btn, current_selection, explanation_box]
    )
    
    # Check answer button
    submit_btn.click(
        check_answer, 
        [accidental_btn, note_btn, chord_type_btn, question_box, explanation_box], 
        [result_box, explanation_box]
    )
    
    # Generate a question on load
    demo.load(
        generate_question, 
        [], 
        [question_box, accidental_btn, note_btn, chord_type_btn, current_selection, explanation_box]
    )

if __name__ == "__main__":
    demo.launch(share=True)
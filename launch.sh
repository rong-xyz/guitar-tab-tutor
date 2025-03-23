#!/bin/bash

# Name of the tmux session
SESSION_NAME="gradio_app"

# Path to your Gradio app
APP_PATH="src/app.py"

# Kill existing session if it exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Killing existing session: $SESSION_NAME"
    tmux kill-session -t $SESSION_NAME
fi

# Create a new tmux session
tmux new-session -d -s $SESSION_NAME

# Send the gradio command to the session
tmux send-keys -t $SESSION_NAME "cd $(pwd) && gradio $APP_PATH" C-m

# Wait for Gradio to start and extract the URLs
sleep 10
tmux capture-pane -t $SESSION_NAME -p > /tmp/gradio_output.txt

# Extract and display the URLs
LOCAL_URL=$(grep "local URL:" /tmp/gradio_output.txt | awk '{print $NF}')
PUBLIC_URL=$(grep "public URL:" /tmp/gradio_output.txt | awk '{print $NF}')

echo "Gradio app started in tmux session: $SESSION_NAME"
echo "Local URL: $LOCAL_URL"
echo "Public URL: $PUBLIC_URL"
echo "To attach to this session: tmux attach -t $SESSION_NAME"
echo "To detach from the session: Ctrl+b followed by d"
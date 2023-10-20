def render_conversations_to_html(conversations, output_file, simulation_ind):
    # Number of agents
    num_agents = len(conversations)

    # Determine if scrolling is needed
    enable_scroll = num_agents > 1

    # Define CSS styles for avatars and chat boxes
    css_styles = '''
    .avatar {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-right: 10px;
        float: left; /* Align avatars to the left */
    }}
    .chat-box {{
        background-color: #f1f0f0;
        padding: 10px;
        margin: 5px;
        border-radius: 10px;
        display: block;
        clear: both; /* Clear the float to prevent overlapping */
        word-wrap: break-word; /* This property wraps long words and text to the next line */
    }}

    .user {{
        background-color: #f0f0f0;
        color: #222;
    }}

    .assistant {{
        background-color: #3498db;
        color: #fff;
    }}

    .conversation-container {{
        display: grid;
        grid-template-columns: repeat({num_agents}, 1fr); /* Create columns for each agent */
        grid-gap: 20px; /* Gap between columns */
        margin-bottom: 20px; /* Add margin between conversation groups */
    }}

    .conversation-title {{
        grid-column: span {num_agents};
        font-weight: bold;
        text-align: center;
        padding-bottom: 20px;
    }}

    .agent-conversation {{
        grid-column: span 1;
        padding-right: 40px;
    }}

    .agent-messages {{
        display: flex;
        flex-direction: row; /* Chat boxes displayed vertically */
    }}
    '''.format(num_agents=num_agents)
    messages_in_line = [[row[i] for row in conversations] for i in range(len(conversations[0]))]
    agent_tiles = ["Agent {} of Case {}".format(ind + 1, simulation_ind + 1) for ind in
                   range(len(conversations))]
    messages_in_line = [agent_tiles] + messages_in_line
    # Initialize the HTML string
    html = '<html><head><style>{}</style></head><body>'.format(css_styles)

    # Create a container for all agents' conversations
    if enable_scroll:
        html += '<div class="scrollable">'
    else:
        html += '<div>'

    for ind, msgs_in_row in enumerate(messages_in_line):
        html += '<div class="row-messages">'
        html += '<div class="conversation-container"> '
        # Create a container for agent's conversation
        for message in msgs_in_row:
            html += '<div class="agent-conversation">'

            if (ind == 0):
                html += '<div class="conversation-title"> {} </div>'.format(message)
            else:
                role = message["role"]
                content = message["content"]

                # Define avatars for user and assistant
                user_avatar = '../images/user.png'  # Replace with the actual path or URL
                assistant_avatar = '../images/robot.jpg'
                # print(ind % 3, role, assistant_avatar)
                # Determine the current avatar based on the role

                current_avatar = user_avatar if role in ["system", "user"] else assistant_avatar

                # Add the avatar image element
                avatar_element = '<img src="{}" class="avatar">'.format(current_avatar)

                # Add the chat box with the avatar and content
                chat_box = '<div class="chat-box {}">{}</div>'.format(role, content)

                # Create a container for agent's messages
                agent_messages = '<div class="agent-messages">{}</div>'.format(avatar_element + chat_box)

                # Add the agent's messages to the agent's conversation
                html += agent_messages
            # Close the agent's conversation container
            html += '</div>'

        # Close the conversation container
        html += '</div>'
        html += '</div>'
    # Close the container for all agents' conversations

    html += '</div>'
    # Close the body and HTML document
    html += '</body></html>'

    # Write the HTML to the specified output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html)

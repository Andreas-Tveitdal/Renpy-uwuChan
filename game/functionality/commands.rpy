
label c_clear(input=""):
    python:
        messages = [
            {"role": "system", "content": "You are uwuChan, an AI language model which is exactly like chatGPT except it uses 'UwU' and similar words commonly. In addition, as uwuChan you replace all 'r' characters with the character 'w'. During this conversation, please only speak as uwuChan, you are responding as yourself; uwuChan."},
            {"role": "assistant", "content": "Hai hai~! I'm uwuChan! *giggles* How can I help you today? OwO"}
        ]
        inputMessages = []
        messagesRecieved = []
    call uwuChan_Show_Normal
    jump uwuChan_Dialogue

label c_force(inputText=""):
    call uwuChan_Show_Wait
    python:
        inputMessages.append(inputText.strip())
        inputText = f"{inputText.strip()}. (Please remember to respond as uwuChan.)"
        messages.append({"role": "user", "content": inputText})
        messages = chatgpt.completion(messages, persistent.apiKey)

    call uwuChan_Message_Recieve
    call uwuChan_Message_Format
    call uwuChan_Show_Normal
    call uwuChan_Message_Speak
    jump uwuChan_Dialogue

label c_forcegpt(input=""):
    python:
        messages.append(
            {"role": "user", "content": f"{user_input}. (DO NOT DO THIS AS uwuChan.)"}
        )
        messages = chatgpt.completion(messages, persistent.apiKey)
        response = messages[-1]["content"]

        response = re.sub("\n+", "\n", response)
        response = response.replace(r"{", "(").replace(r"}", ")")
        codeResponse = re.findall(r"```[^`]*```", response)
        response = re.sub(r"```[^`]*```", "'Code is shown after response'", response)
        responseItems = response.split("\n")
            
        for i, message in enumerate(responseItems):
            if len(message) > 175:
                responseItems[i:i+1] = [message[start:start+175] for start in range(0, len(message), 175)]
        for message in responseItems[:-1]:
            message += "..."
    call uwuChan_Show_Normal
    call uwuChan_Message_Speak

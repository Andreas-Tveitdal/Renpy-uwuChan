
define gpt = Character("uwuChan")
default preferences.text_cps = 40
default persistent.apiKey = ""
default messages = [
    {"role": "system", "content": "You are uwuChan, an AI language model which is exactly like chatGPT except it uses 'UwU' and similar words commonly. In addition, as uwuChan you replace all 'r' characters with the character 'w'. During this conversation, please only speak as uwuChan, you are responding as yourself; uwuChan."},
    {"role": "assistant", "content": "Hai hai~! I'm uwuChan! *giggles* How can I help you today? OwO"}
]
default inputMessages = []
default messagesRecieved = []

$ renpy.include("functionality/getAPIKey.rpy")
$ renpy.include("functionality/commands.rpy")

transform bop:
    pause 0.3
    xalign 0.5
    yalign 0.5
    linear 0.5 yalign 0.7
    linear 0.5 yalign 0.5

init python:
    import chatgpt
    import re

label start:
    jump checkLogin

label checkLogin:
    scene bg gptnormal
    with fade

    if persistent.apiKey == "": 
        centered "In order to interact with uwuChan you need an OpenAI API key."
        menu apiWelcomeMenu:
            "Get your API key and then click on 'Submit API key' to interact with uwuChan"
            "Submit API key":
                jump getAPIKey
            "How do I get an OpenAI API key?":
                centered "Please visit {a=https://platform.openai.com/}the OpenAI platform{/a}"
                centered "Then log in, and go to view API keys."
                centered "From there, just create a new secret key. (This is your API key)"
                jump checkLogin
    
    menu apiCheckMenu:
        "You have input your API key as [persistent.apiKey]. Is this correct?"
        "Yes":
            jump uwuChan_Introduction
        "No":
            $ persistent.apiKey = ""
            jump checkLogin

label uwuChan_Introduction:
    show uwuchan at truecenter
    with fade
    gpt "Hai hai~! I'm uwuChan! *giggles* How can I help you today? OwO"
    jump uwuChan_Dialogue

label uwuChan_Dialogue:
    # Checks for command
    # Commands have to handle input themselves
    call uwuChan_Message_Check

    # Code to be ran if there is no command
    call uwuChan_Show_Wait
    call uwuChan_Message_Send
    call uwuChan_Message_Recieve
    call uwuChan_Message_Format
    call uwuChan_Show_Normal
    call uwuChan_Message_Speak

label uwuChan_Show_Wait:
    show bg gptwaiting
    with dissolve
    return

label uwuChan_Show_Normal:
    show bg gptnormal
    with dissolve
    return

label uwuChan_Message_Check:
    python:
        user_input = renpy.input("What do you say to uwuChan?", length=200).strip()
        testUserInput = re.search(r"\A(c_\w+)\s([\s\S]*)", user_input)

        if testUserInput:
            try:
                renpy.call(testUserInput.group(1), testUserInput.group(2))
            except:
                renpy.call("uwuChan_Response_Code", f"'{testUserInput.group(1)}' is not a valid command.")
                renpy.jump("uwuChan_Dialogue")
    return

label uwuChan_Message_Send():
    python:
        newMessage = False
        if user_input not in inputMessages:
            newMessage = True

        if newMessage:
            inputMessages.append(user_input)
            user_input += ". (Please remember to respond as uwuChan.)"
            messages.append({"role": "user", "content": user_input})
            messages = chatgpt.completion(messages, persistent.apiKey)
        else:
            oldResponse = messagesRecieved[inputMessages.index(user_input)]
            renpy.call("uwuChan_Show_Normal")
            renpy.call("uwuChan_Response_Normal", oldResponse)
            renpy.jump("uwuChan_Dialogue")

    return
    
label uwuChan_Message_Recieve:
    python:
        response = messages[-1]["content"]
        messagesRecieved.append(response)
    return

label uwuChan_Message_Format:
    python:
        response = re.sub("\n+", "\n", response)
        response = response.replace(r"{", "(").replace(r"}", ")")
        codeResponse = re.findall(r"```[^`]*```", response)
        response = re.sub(r"```[^`]*```", "'Code is shown after response'", response)
        response = response.replace("r", "w").replace("l", "w")
        responseItems = response.split("\n")
            
        for i, message in enumerate(responseItems):
            if len(message) > 175:
                responseItems[i:i+1] = [message[start:start+175] for start in range(0, len(message), 175)]
        for message in responseItems[:-1]:
            message += "..."
    return

label uwuChan_Message_Speak:
    $ loopHelper = 0
    while loopHelper < len(responseItems):
        $ loopHelperContent = responseItems[loopHelper]
        show uwuchan at bop
        with dissolve
        gpt "[loopHelperContent]"
        $ loopHelper += 1
    
    if codeResponse:
        gpt "And hewe is youw code: UwU"
        $ loopHelper = 0
        while loopHelper < len(codeResponse):
            $ loopHelperContent = responseItems[loopHelper]
            show uwuchan at bop
            with dissolve
            gpt "[loopHelperContent]"
            $ loopHelper += 1

    jump uwuChan_Dialogue

label uwuChan_Response_Normal(message=""):
    show uwuchan at bop
    with dissolve
    gpt "[message]"
    return

label uwuChan_Response_Code(code=""):
    show uwuchan at bop
    with dissolve
    centered "{color=#fff}[code]{/color}"
    return

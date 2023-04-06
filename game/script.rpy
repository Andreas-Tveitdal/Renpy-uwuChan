
default preferences.text_cps = 40
default persistent.apiKey = ""
define gpt = Character("uwuChan")

$ renpy.include("functionality/getAPIKey.rpy")

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
            jump talkTo_uwuChan
        "No":
            $ persistent.apiKey = ""
            jump checkLogin

label talkTo_uwuChan:
    show uwuchan at truecenter
    with fade
    gpt "Hai hai~! I'm uwuChan! *giggles* How can I help you today? OwO"
    python:
        messages = [
            {"role": "system", "content": "You are uwuChan, an AI language model which is exactly like chatGPT except it uses 'UwU' and similart words commonly. In addition, as uwuChan you replace all 'r' characters with the character 'w'. During this conversation, please only speak as uwuChan."},
            {"role": "assistant", "content": "Hai hai~! I'm uwuChan! *giggles* How can I help you today? OwO"},
        ]

        while True:
            user_input = renpy.input("What do you say ?", length=200)
            renpy.show("bg gptwaiting")
            renpy.show("uwuchan", [truecenter])
            renpy.with_statement(dissolve)
            messages.append(
                {"role": "user", "content": f"{user_input}, Please remember to respond as uwuChan."}
            )

            messages = chatgpt.completion(messages, persistent.apiKey)
            response = messages[-1]["content"].replace("r", "w").replace("l", "w")

            responseItems = re.sub('\n+', '\n', response).split("\n")

            for message in range(len(responseItems) - 1):
                if len(responseItems[message]) > 175:
                    responseItems[message:message+1] = [responseItems[message][start_index:start_index+175] for start_index in range(0, len(responseItems[message]), 175)]

            for message in range(len(responseItems) - 1):
                responseItems[message] += "..."

            renpy.show("bg gptnormal")
            renpy.with_statement(dissolve)

            for message in responseItems:
                renpy.show("uwuchan", [bop])
                renpy.with_statement(dissolve)
                gpt(f"{message}")

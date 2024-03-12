from openai import OpenAI
client = OpenAI(
    api_key="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"
)

def rewrite(content, style, language):
    if language == "English":
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user",
                 "content": content + "Please rewrite it in style of" + style}
            ]
        )
    else:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user",
                 "content": content + "Please translate it into" + language + "in a style of " + style}
            ]
        )

    return completion.choices[0].message.content

# print(rewrite("A Russian dog named Laika was the first animal in space, traveling around Earth in 1957.", "cute", "Japanese"))

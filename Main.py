from openai import OpenAI
import time
key = input("Please enter an openAI API key")
client = OpenAI(api_key=key)
assistant_id = "asst_L5yXZp2250F2EqQjC677qpgm"
print("Opening file")
file_name = "../.venv/test_code.py"
with open(file_name) as f:
    prompt = f.read()
prompt = "file name: " + file_name + " code: " + prompt

thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=prompt
)


def create_thread(assistant_id, prompt):
    # Get Assistant
    assistant = client.beta.assistants.retrieve(assistant_id)
    # create a thread
    thread = client.beta.threads.create()
    my_thread_id = thread.id

    # create a message
    message = client.beta.threads.messages.create(
        thread_id=my_thread_id,
        role="user",
        content=prompt
    )
    # run
    run = client.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=assistant_id,
    )
    return run.id, thread.id


def check_status(run_id, thread_id):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status
print("Writing code")

my_run_id, my_thread_id = create_thread(assistant_id, prompt)
status = check_status(my_run_id, my_thread_id)
while status != "completed":
    status = check_status(my_run_id, my_thread_id)
    time.sleep(2)
response = client.beta.threads.messages.list(
    thread_id=my_thread_id
)
r = response.data[0].content[0].text.value
print(prompt)
if response.data:
    print(r)


with open("../.venv/unit_tests.py", "w") as file:
    file.write(r)

with open("../.venv/unit_tests.py", "r") as file:
    lines = file.readlines()

with open("../.venv/unit_tests.py", "w") as file:
    for number, line in enumerate(lines):
        if number not in [0, len(lines)-1]:
            file.write(line)
print("Done")

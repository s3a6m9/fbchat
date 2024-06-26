import fbchat
import time

session = fbchat.Session.login("EMAIL / NUMBER", "PASSWORD")

client = fbchat.Client(session=session)


print("Messages that are '' mean that they are images")
print("Errors are normal and unsending is retried, the script quits if a message is not unsent.\n")

print(f"Own id: {session.user.id}\n\n")

def unsend_message(message):
    max_attempts = 6
    time_slept = 5
    for attempt in range(max_attempts - 1):
        try:
            message.unsend()
            return
        except Exception as error:
            print(error, "\n\n")
            print("\tERROR, CAUSE\n\t------------\n", message, "\n\n\t RETRYING")
            time.sleep(time_slept)
            time_slept += 1
            if attempt >= max_attempts - 1:
                print("Retried 5 times.\n Quitting.")
                raise


threads = list(client.fetch_threads(limit=None))

for thread in threads:
    print(f"Fetching all messages in {thread.name}")
    skipped_msgs = []

    unsend_sleep_time = 0.6
    skip_count = 200

    delete_count = 1

    for message in thread.fetch_messages(limit=None):
        if message.author == session.user.id \
            and message.unsent is False:

            if len(skipped_msgs) < skip_count:
                skipped_msgs.append(message)
                continue

            if message.text is None and len(message.attachments) == 0:
                continue

            print(f"({thread.name}) Deleting Message ({delete_count}): '{message.text}'")
            
            unsend_message(message)
            time.sleep(unsend_sleep_time)
            delete_count += 1


    
    for message in skipped_msgs:
        print(f"Cleaning up. ({thread.name}) Deleting Message ({delete_count}): '{message.text}'")
        unsend_message(message)
        time.sleep(unsend_sleep_time)
        delete_count += 1

print("\n\n\tFinished deleting.\n\t------------------")

session.logout()

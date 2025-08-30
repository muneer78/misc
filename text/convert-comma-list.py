import subprocess

# Input list of strings with line breaks
input_string = """
deee2847-e23f-4414-a926-eb8af34b4c9e
ba7cb164-d7e2-4c51-ac9c-496a6a4f6470
0deec809-50bd-48a7-8014-94f130c2d31e
2a19dd19-2d05-4b4a-a0bb-638f9d5cdca9
7d393ef4-b480-44c8-85c9-5e86a5f8d8f5
a4d7dd72-daca-45b7-8207-9046d270b9d4
4347466d-a9a7-455b-8acb-cf7aaf455fb8
4b11b8d3-5d79-494a-aa4c-882ab9e74e65
25afe316-b90c-490e-9d87-9f6380179727
7f7e26f6-46aa-44e5-a19b-92cd655ebb30
ae4cee3f-791f-4152-ade2-1084cc1e2f84
aeef7bff-4c85-49ad-9cf2-5efa741a2305
573f413e-d910-419a-850f-294bfa68a27d
efd7cc6e-06a4-4418-8cf1-cf60a6d083fc
2abf9cae-0fa8-490d-8b0b-38d4687e13ed
d371fbed-0bd8-46a4-8213-3e067b87b24c
c8d5d641-9aeb-462a-8825-2059069b8f48
8558fe1a-a38d-499a-944c-6a7fd7a0a2e7
b7ab42f9-3169-40d3-83e2-bf196ef42c8b
54d11f52-66d6-4714-add6-f0d3863b4d72
4812b6e5-7a6e-4099-b295-4e57a5c3c2db
d53228ee-d3c5-4b7c-9798-a1ecc4c085ce
595d1afd-2ae6-4cf6-8406-456ee49d4851
e817c57b-2565-407d-97b4-efb1ce785ac2
deee2847-e23f-4414-a926-eb8af34b4c9e
50940718-c612-4d8a-ba6f-71d66c26cfa7
b0b6db9d-d6cc-4e8e-8140-7aa5370f5d73
0deec809-50bd-48a7-8014-94f130c2d31e
bdc1558e-c8e9-492e-ba7a-639d8fb07c57
6285778e-0c77-4840-9fb5-5ec292bd1772
7d393ef4-b480-44c8-85c9-5e86a5f8d8f5
c243e1f6-14c4-43ca-b0e9-3c42b4733bf7
be248c57-118f-4829-89b4-b2bfb9af66f8
ad9502b8-930f-48ea-a92f-f7859fb6b977
ba7cb164-d7e2-4c51-ac9c-496a6a4f6470
5357d066-b9a1-4252-9aae-7a5944a5a9cb
25afe316-b90c-490e-9d87-9f6380179727
0b2f58a2-f5a3-4676-891d-34c795f354fe
77566b7c-aca5-4f25-bd59-e39ae5aa52ea
ae4cee3f-791f-4152-ade2-1084cc1e2f84
00c1ee82-2ffc-4255-9159-92326ab4ae77
290f4e9c-f8da-4bdd-ad69-2cc3ef4996e9
f5abb9bd-0e2f-4239-bc96-d16e4c434184
2db11be2-f827-4472-b405-b3ea40236f65
a60842a6-11b5-4ed9-bc6a-5a1cbeb67237
efd7cc6e-06a4-4418-8cf1-cf60a6d083fc
39fe74fd-8c48-4d05-a09d-bda738dcc121
ebc9dbc1-1396-42ac-b41a-031968330b7c
bd8c23a6-e482-4a03-b8af-4b729d133de0
3718d429-9948-47b7-8dbd-d022b70c8b58
5251d8f4-1fbe-4d46-8e26-958a82329bda
d371fbed-0bd8-46a4-8213-3e067b87b24c
a9b49612-6b13-4c40-8db4-e0ac5d21df1f
0de3655d-bffe-4a17-9d83-c04f90c1d010
2d0336e3-ebe3-4a03-ba99-a836de6f7541
c80070a5-9a08-4336-97b8-f484daacfcc8
35adfe72-9138-49c6-ad1b-74392efa9a35
aeef7bff-4c85-49ad-9cf2-5efa741a2305
409c4934-c9a2-4834-a444-ef4efc945a53
54d11f52-66d6-4714-add6-f0d3863b4d72
0e06ccb9-928b-4564-9723-54d0a061bddb
13742130-696b-4816-a020-f918c4464bed
"""


def copy2clip(txt):
    cmd = "echo " + txt.strip() + "|clip"
    return subprocess.check_call(cmd, shell=True)


# # Split the input into a list of strings without quotes around each item
# strings_list = input_string.strip().split("\n")
# result = ", ".join(strings_list)

# Split the input into a list of strings with quotes around each item
strings_list = input_string.strip().split("\n")
formatted_list = [f"'{name}'" for name in strings_list]
result = ", ".join(formatted_list)

# Print the result to the terminal
print(result)

# Copy to the clipboard
copy2clip(result)

# # Enclose the result in parentheses
# final_result = f"({result})"

# # Print paren enclosed result to the terminal
# print(final_result)

# # Copy paren enclosed result to the clipboard
# copy2clip(final_result)

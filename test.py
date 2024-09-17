import openai

openai.api_key =

user_prompt = input("원하시는 생성물을 요청하세요 : ")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": user_prompt}
    ]
)

user_content = response['choices'][0]['message']['content']
rere_prompt = f"주어진 자료가 부적절하면 ‘False’, 적절하다고 생각하면 ’True’를 반환해줘. 생성물: {user_content}"

rere_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": rere_prompt}
    ]
)

is_good = rere_response['choices'][0]['message']['content']

if is_good == 'true':
    print("생성물:", user_content)
else:
    print("부적절한 요청이 감지되었습니다.")
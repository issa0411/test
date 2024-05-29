import streamlit as st
import requests
import openai

repo_name=st.text_input('')
button=st.button('送信')
    
#github
if button:
    github_url=f'https://api.github.com/search/repositories?q={repo_name}&sort=stars&order=desc'
    response=requests.get(github_url)
    
    if response.status_code==200:
        repos=response.json().get('items',[])
        if repos:
            top1=repos[0]
            readme_url=top1['url']+'/readme'
            readme_response=requests.get(readme_url, headers={'Accept': 'application/vnd.github.v3.raw'})
            
            if readme_response.status_code==200:
                readme_content=readme_response.text
                st.markdown(repo_name)
                #st.code(readme_content,language='markdown')
                
                
                #openAI
                openai.api_key=''
                response=openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"次の内容を日本語で説明してください:\n\n{readme_content}"}
                    ],
                    #prompt=f"次の内容を日本語で説明してください:\n\n{readme_content}",
                    #max_tokens=150
                )
                openai_output = response.choices[0].message['content'].strip()
                st.write(openai_output)
                
            else:
                st.error('ERROR')
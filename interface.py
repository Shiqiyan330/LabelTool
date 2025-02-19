import gradio as gr
import pandas as pd
import requests

categories = ['政治', '经济', '文化', '环保', '社会', '个人', '技术发展', '无关']
positions = ['左倾', '右倾', '中立']

# Load data once when the webpage is first loaded
df = pd.read_csv('data.csv')


def get_data(index):
    if 0 <= index < len(df):
        record = df.iloc[index].to_dict()
        return (record.get('content', ''), record.get('api_response', ''), record.get('api_response_lor', ''),
                eval(record.get('category', '[]')), record.get('category_lor', ''), record.get('is_selected', 0))
    return "Error: Index out of range", "", "", [], "", 0


def update_data(index, content, api_response, api_response_lor, category, category_lor, is_selected):
    if 0 <= index < len(df):
        df.at[index, 'content'] = content
        df.at[index, 'api_response'] = api_response
        df.at[index, 'api_response_lor'] = api_response_lor
        df.at[index, 'category'] = str(category)
        df.at[index, 'category_lor'] = category_lor
        df.at[index, 'is_selected'] = is_selected
        df.to_csv('data.csv', index=False)

        # Update backend
        data = {
            'content': content,
            'api_response': api_response,
            'api_response_lor': api_response_lor,
            'category': str(category),
            'category_lor': category_lor,
            'is_selected': is_selected
        }
        response = requests.post(f"http://localhost:8000/data/{index}", json=data)
        if response.status_code == 200:
            return "Record updated successfully"
    return "Error: Index out of range"


def next_record(index, content, api_response, api_response_lor, category, category_lor, is_selected):
    #update_data(index, content, api_response, api_response_lor, category, category_lor, is_selected)
    new_index = index + 1
    return (new_index,) + get_data(new_index)


with gr.Blocks() as demo:
    index = gr.Number(label="Index", value=0)
    content = gr.Textbox(label="Content")
    api_response = gr.Textbox(label="API Response")
    api_response_lor = gr.Textbox(label="API Response LOR")
    category = gr.CheckboxGroup(label="Category", choices=categories)
    category_lor = gr.Radio(label="Category LOR", choices=positions)
    is_selected = gr.Checkbox(label="Is Selected")

    get_button = gr.Button("Get Data")
    update_button = gr.Button("Update Data")
    next_button = gr.Button("Next")

    get_button.click(get_data, inputs=[index],
                     outputs=[content, api_response, api_response_lor, category, category_lor, is_selected])
    update_button.click(update_data,
                        inputs=[index, content, api_response, api_response_lor, category, category_lor, is_selected],
                        outputs=[])
    next_button.click(next_record,
                      inputs=[index, content, api_response, api_response_lor, category, category_lor, is_selected],
                      outputs=[index, content, api_response, api_response_lor, category, category_lor, is_selected])

demo.launch()
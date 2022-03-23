defmodule Schwi.Lib.GPT3 do
  def get_completion(prompt) do
    token = System.get_env("OPENAI_KEY")
    url = "https://api.openai.com/v1/engines/text-davinci-002/completions"

    headers = [
      Authorization: "Bearer #{token}",
      Accept: "Application/json; Charset=utf-8",
      "Content-Type": "application/json"
    ]

    {:ok, body} = JSON.encode(prompt: prompt, max_tokens: 64)

    {:ok, %HTTPoison.Response{status_code: 200, body: response_raw}} =
      HTTPoison.post(url, body, headers)

    {:ok, response} = JSON.decode(response_raw)
    # Get choices[0].text if choices is not empty
    choices = response["choices"]

    if Enum.count(choices) > 0 do
      String.trim(List.first(choices)["text"])
    else
      nil
    end
  end
end

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
    res = HTTPoison.post(url, body, headers)

    case res do
      {:ok, %HTTPoison.Response{status_code: 200, body: response_raw}} ->
        {:ok, response} = JSON.decode(response_raw)

        choices = response["choices"]

        if Enum.count(choices) > 0 do
          {:ok, String.trim(List.first(choices)["text"])}
        else
          {:error, "No completion found"}
        end

      {:ok, %HTTPoison.Response{status_code: response_code}} ->
        {:error, "HTTP #{response_code}"}

      _ ->
        {:error, "Unknown error"}
    end
  end
end

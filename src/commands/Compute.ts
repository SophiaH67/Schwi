import Command from "../../../eris-boreas/src/conversation/Command";
import Conversation from "../../../eris-boreas/src/conversation/Conversation";
import { success } from "../lib/transformer";
import OpenAI from "openai-api";
import assert from "assert";

export default class Compute implements Command {
  public aliases = [
    "compute",
    "what",
    "who",
    "why",
    "when",
    "where",
    "how",
    "can",
  ];
  public description = "GPT3 compute";
  public usage = "compute <prompt>";
  private openai = new OpenAI(
    process.env.OPENAI_KEY || assert("OPENAI_KEY") || ""
  );

  public async run(conversation: Conversation, args: string[]) {
    let prompt: string;
    if (args[0].toLowerCase() === "compute") {
      prompt = args.slice(1).join(" ");
    } else {
      prompt = args.join(" ");
    }
    prompt = prompt + "\n";

    const gptResponse = await this.openai.complete({
      engine: "text-davinci-002",
      prompt,
      maxTokens: 64,
    });
    let text = gptResponse.data.choices[0].text;
    text = text.trim();

    return success(text);
  }
}

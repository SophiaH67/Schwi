import Command from "eris-boreas/lib/src/conversation/Command";
import Conversation from "eris-boreas/lib/src/conversation/Conversation";
import { success } from "../lib/transformer";
import { Configuration, OpenAIApi } from "openai";
import ContextManager from "../lib/ContextManager";

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
    "should",
    "write",
    "which",
    "do i",
    "explain",
    "does",
    "is that",
    "is it",
    "is this",
    "schwi",
  ];
  public description = "GPT3 compute";
  public usage = "compute <prompt>";
  private config: Configuration = new Configuration({
    apiKey: process.env.OPENAI_KEY,
  });
  private openai: OpenAIApi = new OpenAIApi(this.config);

  public async run(conversation: Conversation, _args: string[]) {
    const contextManager = new ContextManager(conversation.eris);
    const prompt = await contextManager.get(conversation.messages[0]);

    let usernames: Set<string> = new Set();

    prompt.reverse();

    // Add `Bot:`
    prompt.push(`${conversation.eris.bot.user?.username}:`);

    prompt.forEach((p) => {
      if (usernames.size >= 4) return;
      const username = p.split(":")[0];

      if (username) {
        usernames.add(username);
      }
    });

    const gptResponse = await this.openai
      .createCompletion("text-davinci-002", {
        prompt: prompt.join("\n"),
        max_tokens: 64,
        stop: [...usernames].map((u) => `${u}:`),
        temperature: 0.8,
      })
      .catch((e) => {
        // e is instanceof a axios error
        if (e.isAxiosError) {
          console.error(e);
          console.log(e.request?.data);
          console.log(e.response?.data);
        } else {
          throw e;
        }
      });

    let text = gptResponse?.data?.choices?.[0]?.text;
    if (!text) return;

    text = text.trim();
    text = text.replace(/\n/g, " ");

    while (text.includes("  ")) {
      text = text.replace("  ", " ");
    }

    text = contextManager.replaceUsernamesWithMentions(text);

    // If it contains a : in the first 4 words, return it
    if (text.split(" ").slice(0, 4).join(" ").includes(":")) {
      return text;
    } else {
      return success(text); // Add the : thing
    }
  }
}

import Command from "eris-boreas/lib/src/conversation/Command";
import Conversation from "eris-boreas/lib/src/conversation/Conversation";
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
    "should",
    "write",
    "which",
    "do i",
    "explain",
    "does",
    "is that",
    "is it",
    "is this",
  ];
  public description = "GPT3 compute";
  public usage = "compute <prompt>";
  private openai = new OpenAI(
    process.env.OPENAI_KEY || assert("OPENAI_KEY") || ""
  );

  public async run(conversation: Conversation, args: string[]) {
    let current: string;
    if (args[0].toLowerCase() === "compute") {
      current = args.slice(1).join(" ");
    } else {
      current = args.join(" ");
    }

    const prompt = await conversation.eris.redis.lRange(
      `schwi:context:${conversation.messages[0].channelId}`,
      0,
      -1
    );

    let usernames: Set<string> = new Set();

    prompt
      .reverse()
      // Remove last item, which is the current message
      .pop();
    // Add current message
    prompt.push(`${conversation.messages[0].author.username}: ${current}`);
    // Add `Bot:`
    prompt.push(`${conversation.eris.bot.user?.username}:`);

    prompt.forEach((p) => {
      const username = p.split(":")[0];
      if (username) {
        usernames.add(username);
      }
    });

    const gptResponse = await this.openai.complete({
      engine: "text-davinci-002",
      prompt: prompt.join("\n"),
      maxTokens: 64,
      stop: [...usernames].map((u) => `${u}:`),
      temperature: 0.8,
    });

    let text = gptResponse.data.choices[0].text;
    text = text.trim();

    // If it contains a : in the first 4 words, return it
    if (text.split(" ").slice(0, 4).join(" ").includes(":")) {
      return text;
    } else {
      return success(text); // Add the : thing
    }
  }
}

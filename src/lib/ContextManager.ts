import { ErisClient } from "eris-boreas";
import { Message } from "discord.js";

export default class ContextManager {
  constructor(public schwi: ErisClient) {}
  public async get(message: Message<boolean>) {
    const prompt = await this.schwi.redis.lRange(
      `schwi:context:${message.channelId}`,
      0,
      -1
    );
    return prompt;
  }

  public async add(message: Message<boolean>) {
    console.log("Adding to context:", message.content);
    const last = await this.schwi.redis.lRange(
      `schwi:context:${message.channelId}`,
      -1,
      -1
    );
    if (last.length !== 0) {
      let [username, text] = last[0].split(":");
      if (username === message.author.username) {
        // Update the last item in the list to add the current message
        await this.schwi.redis.lSet(
          `schwi:context:${message.channelId}`,
          -1,
          `${
            message.author.username
          }: ${text}\n${this.replaceMentionsWithUsernames(message.content)}`
        );
      } else {
        this._addToContext(message);
      }
    } else {
      this._addToContext(message);
    }
    // await schwi.redis.lTrim(`schwi:context:${message.channelId}`, 0, 9);
  }

  private async _addToContext(message: Message<boolean>) {
    return await this.schwi.redis.lPush(
      `schwi:context:${message.channelId}`,
      `${message.author.username}: ${this.replaceMentionsWithUsernames(
        message.content
      )}`
    );
  }

  public async replaceMentionsWithUsernames(message: string) {
    const mentions = message.match(/<@!?(\d+)>/g);
    if (mentions) {
      for (const mention of mentions) {
        const id = mention.match(/\d+/)?.[0];
        if (!id) continue;
        const user = await this.schwi.bot.users.fetch(id);
        message = message.replace(mention, `@"${user.username}"`);
      }
    }
  }

  public replaceUsernamesWithMentions(message: string) {
    const usernames = message.match(/@"(.*?)"/g);
    if (usernames) {
      for (const username of usernames) {
        const user = this.schwi.bot.users.cache.find(
          (u) => u.username.toLowerCase() === username.toLowerCase()
        );
        if (!user) continue;
        message = message.replace(username, `<@${user.id}>`);
      }
    }
    return message;
  }
}

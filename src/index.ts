require("dotenv").config();
import { ErisClient } from "eris-boreas";
import { Client, Intents, Message } from "discord.js";

class Schwi extends ErisClient {
  get name() {
    return "Schwi";
  }

  public async onReady(): Promise<void> {
    // Load all commands from ./commands
    this.loadCommands(__dirname + "/commands");
    super.onReady();
  }

  public async onMessage(msg: Message<boolean>): Promise<void> {
    await this.redis.LPUSH(
      `schwi:context:${msg.channelId}`,
      `${msg.author.username}: ${msg.content}`
    );

    // // Expire after 30 minutes
    // await this.redis.EXPIRE(`schwi:context:${msg.channelId}`, 60 * 30);
    // LTRIM to keep the list at most 10 items
    await this.redis.lTrim(`schwi:context:${msg.channelId}`, 0, 9);

    await super.onMessage(msg);
  }
}

const discordClient = new Client({
  intents: [
    Intents.FLAGS.GUILDS,
    Intents.FLAGS.GUILD_MESSAGES,
    Intents.FLAGS.GUILD_MESSAGE_REACTIONS,
    Intents.FLAGS.GUILD_MESSAGE_TYPING,
    Intents.FLAGS.DIRECT_MESSAGES,
    Intents.FLAGS.DIRECT_MESSAGE_REACTIONS,
    Intents.FLAGS.DIRECT_MESSAGE_TYPING,
  ],
  partials: [
    "CHANNEL", // Required to receive DMs
  ],
});
const client = new Schwi(discordClient);
client.bot.login(process.env.DISCORD_TOKEN);

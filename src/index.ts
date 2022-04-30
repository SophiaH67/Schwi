import "dotenv/config";
import { ErisClient } from "eris-boreas";
import { Client, Intents } from "discord.js";

class Schwi extends ErisClient {
  get name() {
    return "Schwi";
  }

  public async onReady(): Promise<void> {
    // Load all commands from ./commands
    this.loadCommands(__dirname + "/commands");
    super.onReady();
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

import Command from "eris-boreas/lib/src/conversation/Command";
import Conversation from "eris-boreas/lib/src/conversation/Conversation";
import { success } from "../lib/transformer";

export default class Reds implements Command {
  public aliases = ["redis", "set", "get", "del"];
  public description = "Send a message to Redis";
  public usage = "redis <command> <key> <value>";

  public async run(conversation: Conversation, args: string[]) {
    if (args[0].toLowerCase() == "redis") {
      args.shift();
    }
    const command = args.shift() || "";
    const redis = conversation.eris.redis;

    if (command.toLowerCase() == "set") {
      //@ts-ignore
      return success(await redis.set(args.shift(), args.join(" ")));
    } else if (command.toLowerCase() == "get") {
      //@ts-ignore
      return success(await redis.get(args.join(" ")));
    } else if (command.toLowerCase() == "del") {
      //@ts-ignore
      return success((await redis.del(args.join(" "))).toString());
    } else {
      throw new Error("Invalid redis command");
      return ""; // never reached but typescript complains
    }
  }
}

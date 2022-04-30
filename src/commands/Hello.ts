import Command from "eris-boreas/lib/src/conversation/Command";
import Conversation from "eris-boreas/lib/src/conversation/Conversation";
import { info } from "../lib/transformer";

export default class Hello implements Command {
  public aliases = ["hello", "oh h", "hey", "hi", "oha"];
  public description = ":hello:";
  public usage = "Hello!";

  public async run(_conversation: Conversation, _args: string[]) {
    return info(["Hello", "Hi", "Konbanwa", "Ohayo"]);
  }
}

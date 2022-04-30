import Command from "eris-boreas/lib/src/conversation/Command";
import Conversation from "eris-boreas/lib/src/conversation/Conversation";
import { info } from "../lib/transformer";

export default class Thanks implements Command {
  public aliases = ["thank", "tskr"];
  public description = "Glad I could help";
  public usage = "Thanks!";

  public async run(_conversation: Conversation, _args: string[]) {
    return info([
      "I don't know what I did, but no problem",
      "You're welcome?",
      "No problem",
    ]);
  }
}

import { ErisClient } from "eris-boreas";
import { SentimentAnalyzer, PorterStemmer, WordTokenizer } from "natural";
import compromise from "compromise";
import { Message } from "discord.js";
//@ts-expect-error
import * as autocorrecti from "autocorrect";
const autocorrect = autocorrecti.default() as (text: string) => string;

export interface UserProfile {
  id: string; // Discord ID
  preferences: { [key: string]: number }; // ["Ice Cream": 0.2, "Coffee": 0.3, "Outside": -0.4]
}
export default class UserProfileManager {
  private tokenizer = new WordTokenizer();
  private analyzer = new SentimentAnalyzer("English", PorterStemmer, "afinn");

  constructor(public schwi: ErisClient) {}

  public async get(userId: string): Promise<UserProfile> {
    const profileJSON = await this.schwi.redis.get(`schwi:user:${userId}`);
    const profile = JSON.parse(profileJSON || "null");
    if (!profile) {
      return await this.create(userId);
    }
    return profile as UserProfile;
  }

  public async create(userId: string): Promise<UserProfile> {
    const profile = {
      id: userId,
      preferences: {},
    };
    await this.schwi.redis.set(`schwi:user:${userId}`, JSON.stringify(profile));
    return profile;
  }

  public async update(profile: UserProfile): Promise<void> {
    // Cap the values to [-1, 1]
    for (const key in profile.preferences) {
      profile.preferences[key] = Math.min(
        1,
        Math.max(-1, profile.preferences[key])
      );
    }
    await this.schwi.redis.set(
      `schwi:user:${profile.id}`,
      JSON.stringify(profile)
    );
  }

  public async handleMessage(message: Message<boolean>) {
    const profile = await this.get(message.author.id);
    const oProfile = JSON.parse(JSON.stringify(profile));

    const doc = compromise(message.content);
    if (doc.sentences().length === 0) return;
    await Promise.all(
      doc.sentences().map((m) => this.handleSentence(m.text(), profile))
    );
    if (JSON.stringify(oProfile) !== JSON.stringify(profile)) {
      await this.update(profile);
    }
  }

  public async handleSentence(sentence: string, profile: UserProfile) {
    const words = this.tokenizer.tokenize(sentence);
    const sentiment = this.analyzer.getSentiment(words);
    const doc = compromise(sentence);
    let nouns = doc.nouns();
    let toRemove: string[] = doc.pronouns().out("array");
    toRemove = toRemove.concat(doc.adjectives().out("array")); // probably doesn't work
    toRemove = toRemove.concat(doc.adverbs().out("array")); // probably doesn't work

    const filteredNouns: string[] = nouns
      .toSingular()
      .filter((n) => !toRemove.includes(n.out("text")))
      .dehyphenate()
      .out("array")
      .map((word: string) => word.split(" ").map(autocorrect).join(" "));

    for (const noun of filteredNouns) {
      if (profile.preferences[noun]) {
        profile.preferences[noun] += sentiment;
      } else {
        profile.preferences[noun] = sentiment;
      }
    }
  }
}

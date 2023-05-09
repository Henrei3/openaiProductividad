export class Gestion {
  constructor(
        public id ? : Number,
        public audio_text? : JSON,
        public gpt_answer? : JSON,
        public patterns? : JSON,
        public score? : JSON
    ) {}
}

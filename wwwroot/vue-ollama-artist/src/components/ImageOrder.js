class ImageOrder {
    constructor({
                    Text = "",
                    Style = "",
                    Age = 0,
                    Seed = 0,
                    Width = 720,
                    Height = 720
                } = {}) {
        this.Text = Text;
        this.Style = Style;
        this.Age = Age;
        this.Seed = Seed;
        this.Width = Width;
        this.Height = Height;
    }

    toJSON() {
        return JSON.stringify({
            Text: this.Text,
            Style: this.Style,
            Age: this.Age,
            Seed: this.Seed,
            Width: this.Width,
            Height: this.Height
        });
    }

    static toStringPromptFormat() {
        return "Text: string, Style: string, Age: number, Seed: number, Width: number, Height: number";
    }

    toPrompt() {
        let prompt = `${this.Text}, ((${this.Style}))`;
        if (this.Age > 0) {
            prompt += `, aged by ${this.Age} years`;
        }
        return prompt;
    }
}

export default ImageOrder;
function Sprite(url, x, y, width, height, speed, frames, dir, once) {
    this.url = url;
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.speed = speed;
    this.frames = frames;
    this.once = once;
    this.dir = dir || 'right';
    this._index = 0;

    this.render = function render(ctx) {
        var max,
            idx,
            frame,
            x,
            y;

        if (this.speed > 0 && !this.done) {
            max = this.frames.length - 1;
            idx = Math.floor(this._index);
            frame = this.frames[idx % max];

            if (this.once && idx >= max) {
                this.done = true;
                return;
            }
        } else {
            frame = 0;
        }


        x = this.x;
        y = this.y;

        if (this.dir == 'right') {
            x += frame * this.width;
        } else if (this.dir == 'left') {
            x -= frame * this.width;
        } else if (this.dir === 'down') {
            y += frame * this.height;
        } else if (this.dir === 'up') {
            y -= frame * this.height;
        }

        ctx.drawImage(
            Image.get(this.url),
            x, y,
            this.width, this.height,
            0, 0,
            this.width, this.height
        );
    };

    this.update = function update(dt) {
        this._index += this.speed * dt;
    };
}

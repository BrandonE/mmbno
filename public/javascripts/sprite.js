function Sprite(path, x, y, width, height, speed, frames, spacing, direction, once) {
    this.path = path;
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.speed = speed;
    this.frames = frames;
    this.spacing = spacing;
    this.once = once;
    this.direction = direction || 'right';
    this._index = 0;

    this.render = function render(ctx) {
        var x = this.x,
            y = this.y,
            index,
            frame;

        if (this.speed && this.frames && this.spacing) {
            index = Math.floor(this._index);
            frame = this.frames[index % this.frames.length];

            if (this.direction == 'right') {
                x += frame * this.spacing;
            } else if (this.direction == 'left') {
                x -= frame * this.spacing;
            } else if (this.direction === 'down') {
                y += frame * this.spacing;
            } else if (this.direction === 'up') {
                y -= frame * this.spacing;
            }

            if (this.once && index >= this.frames.length - 1) {
                this.done = true;
            }
        }

        ctx.drawImage(
            Image.get(this.path),
            x, y,
            this.width, this.height,
            0, 0,
            this.width, this.height
        );
    };

    this.update = function update(dt) {
        if (!this.done) {
            this._index += this.speed * dt;
        }
    };
}

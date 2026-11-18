/** Playback owns only time and position; mathematics comes from Python. */
export class Playback {
  constructor(length, update, clock = globalThis) { this.length = length; this.update = update; this.clock = clock; this.index = -1; this.timer = null; this.speed = 1; }
  emit() { this.update(this.index, this.timer !== null); }
  pause() { if (this.timer !== null) this.clock.clearInterval(this.timer); this.timer = null; this.emit(); }
  seek(index) { this.pause(); this.index = Math.max(-1, Math.min(this.length - 1, index)); this.emit(); }
  next() { this.seek(this.index + 1); }
  previous() { this.seek(this.index - 1); }
  restart() { this.seek(-1); }
  play() {
    if (this.timer !== null) return;
    if (this.index === this.length - 1) this.index = -1;
    this.timer = this.clock.setInterval(() => {
      this.index++;
      if (this.index >= this.length - 1) this.pause(); else this.emit();
    }, 1400 / this.speed);
    this.emit();
  }
  setSpeed(speed) { const playing = this.timer !== null; this.pause(); this.speed = speed; if (playing) this.play(); }
}

function Video(title, duration) {
    this.title = title;
    this.duration = duration;
}

Video.prototype.getTitle = function () {
    return this.title;
};

Video.prototype.getDuration = function () {
    return this.duration;
};

/*==============================================================*/

function Film(title, duration, genre) {
    Video.call(this, title, duration);

    this.genre = genre;
}

Film.prototype = Object.create(Video.prototype);

Film.prototype.constructor = Film;

Film.prototype.getGenre = function () {
    return this.genre;
};

function durationDecorator(fn) {
    return function () {
    const duration = fn.call(this);
    return `${duration} m.`;
    };
}

Video.prototype.getDuration = durationDecorator(Video.prototype.getDuration);

/*==============================================================*/

const video = new Video("Introduction to Cinema", 120);
console.log("Video Title:", video.getTitle());
console.log("Video Duration:", video.getDuration());

const film = new Film("Inception", 180, "Sci-Fi");
console.log("Film Title:", film.getTitle());
console.log("Film Duration:", film.getDuration());
console.log("Film Genre:", film.getGenre());
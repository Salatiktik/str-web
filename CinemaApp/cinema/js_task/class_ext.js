class Video {
    constructor(title, duration) {
    this.title = title;
    this.duration = duration;
    }

    getTitle() {
    return this.title;
    }

    getDuration (){
    return this.duration;
    }

    getDuration = durationDecorator(this.getDuration)
}

class Film extends Video {
    constructor(title, duration, genre) {
    super(title, duration);
    this.genre = genre;
    }

    getGenre() {
    return this.genre;
    }
}


function durationDecorator(descriptor) {
    const originalMethod = descriptor;

    descriptor = function () {
    const duration = originalMethod.call(this);
    return `${duration} m.`;
    };

    return descriptor;
}

const video = new Video("Introduction to Cinema", 120);
console.log("Video Title:", video.getTitle());
console.log("Video Duration:", video.getDuration());

const film = new Film("Inception", 180, "Sci-Fi");
console.log("Film Title:", film.getTitle());
console.log("Film Duration:", film.getDuration());
console.log("Film Genre:", film.getGenre());
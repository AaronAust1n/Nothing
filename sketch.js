let creatures = [];
let predators = [];
let food = [];

function setup() {
  createCanvas(windowWidth, windowHeight);
  for (let i = 0; i < 50; i++) {
    creatures.push(new Creature(random(width), random(height)));
  }
  for (let i = 0; i < 5; i++) {
    predators.push(new Predator(random(width), random(height)));
  }
  for (let i = 0; i < 100; i++) {
    food.push(createVector(random(width), random(height)));
  }
}

function draw() {
  background(0, 10);

  if (random(1) < 0.1) {
    food.push(createVector(random(width), random(height)));
  }

  for (let i = food.length - 1; i >= 0; i--) {
    fill(0, 255, 0);
    noStroke();
    ellipse(food[i].x, food[i].y, 4, 4);
  }

  for (let i = creatures.length - 1; i >= 0; i--) {
    creatures[i].behaviors(predators, food);
    creatures[i].update();
    creatures[i].display();

    if (creatures[i].isDead()) {
      creatures.splice(i, 1);
    } else if (creatures[i].shouldReproduce()) {
      creatures.push(creatures[i].reproduce());
    }
  }

  for (let i = predators.length - 1; i >= 0; i--) {
    predators[i].hunt(creatures);
    predators[i].update();
    predators[i].display();
    if (predators[i].isDead()) {
      predators.splice(i, 1);
    }
  }
}

class Creature {
  constructor(x, y, dna) {
    this.pos = createVector(x, y);
    this.vel = p5.Vector.random2D();
    this.acc = createVector();
    this.dna = dna || {
      maxSpeed: random(2, 5),
      maxForce: random(0.1, 0.5),
      vision: random(50, 150),
      reproductionRate: random(0.001, 0.005)
    };
    this.health = 1;
  }

  behaviors(predators, food) {
    let steerFlee = this.flee(predators);
    let steerEat = this.eat(food, 0.3);

    steerFlee.mult(5); // Fleeing is a high priority

    this.applyForce(steerFlee);
    this.applyForce(steerEat);
  }

  flee(predators) {
    let record = Infinity;
    let closest = null;
    for (let predator of predators) {
      let d = this.pos.dist(predator.pos);
      if (d < record) {
        record = d;
        closest = predator;
      }
    }

    if (closest && record < this.dna.vision) {
      let desired = p5.Vector.sub(this.pos, closest.pos);
      desired.setMag(this.dna.maxSpeed);
      let steer = p5.Vector.sub(desired, this.vel);
      steer.limit(this.dna.maxForce);
      return steer;
    }
    return createVector(0, 0);
  }

  eat(list, nutrition) {
    let record = Infinity;
    let closest = null;
    for (let i = list.length - 1; i >= 0; i--) {
      let d = this.pos.dist(list[i]);
      if (d < record) {
        record = d;
        closest = i;
      }
    }

    if (record < 5) {
      list.splice(closest, 1);
      this.health += nutrition;
    } else if (closest !== null && record < this.dna.vision) {
      return this.seek(list[closest]);
    }
    return createVector(0, 0);
  }

  seek(target) {
    let desired = p5.Vector.sub(target, this.pos);
    desired.setMag(this.dna.maxSpeed);
    let steer = p5.Vector.sub(desired, this.vel);
    steer.limit(this.dna.maxForce);
    return steer;
  }

  update() {
    this.health -= 0.005;
    this.vel.add(this.acc);
    this.vel.limit(this.dna.maxSpeed);
    this.pos.add(this.vel);
    this.acc.mult(0);
    this.edges();
  }

  applyForce(force) {
    this.acc.add(force);
  }

  isDead() {
    return this.health < 0;
  }

  shouldReproduce() {
    return random(1) < this.dna.reproductionRate;
  }

  reproduce() {
    let childDNA = {
      maxSpeed: this.dna.maxSpeed + random(-0.1, 0.1),
      maxForce: this.dna.maxForce + random(-0.05, 0.05),
      vision: this.dna.vision + random(-10, 10),
      reproductionRate: this.dna.reproductionRate + random(-0.0005, 0.0005)
    };
    return new Creature(this.pos.x, this.pos.y, childDNA);
  }

  edges() {
    if (this.pos.x > width) this.pos.x = 0;
    if (this.pos.x < 0) this.pos.x = width;
    if (this.pos.y > height) this.pos.y = 0;
    if (this.pos.y < 0) this.pos.y = height;
  }

  display() {
    let gr = color(0, 255, 0);
    let rd = color(255, 0, 0);
    let col = lerpColor(rd, gr, this.health);

    stroke(col);
    strokeWeight(map(this.dna.maxSpeed, 2, 5, 2, 6));
    point(this.pos.x, this.pos.y);
  }
}

class Predator {
  constructor(x, y) {
    this.pos = createVector(x, y);
    this.vel = p5.Vector.random2D();
    this.acc = createVector();
    this.maxSpeed = 3;
    this.maxForce = 0.2;
    this.r = 10;
    this.health = 1;
  }

  hunt(creatures) {
    let record = Infinity;
    let closest = null;
    for (let i = creatures.length - 1; i >= 0; i--) {
      let d = this.pos.dist(creatures[i].pos);
      if (d < record) {
        record = d;
        closest = i;
      }
    }

    if (record < 5) {
      creatures.splice(closest, 1);
      this.health += 0.5;
    } else if (closest !== null) {
      this.applyForce(this.seek(creatures[closest]));
    }
  }

  seek(target) {
    let desired = p5.Vector.sub(target.pos, this.pos);
    desired.setMag(this.maxSpeed);
    let steer = p5.Vector.sub(desired, this.vel);
    steer.limit(this.maxForce);
    return steer;
  }

  update() {
    this.health -= 0.01;
    this.vel.add(this.acc);
    this.vel.limit(this.maxSpeed);
    this.pos.add(this.vel);
    this.acc.mult(0);
    this.edges();
  }

  applyForce(force) {
    this.acc.add(force);
  }

  isDead() {
    return this.health < 0;
  }

  edges() {
    if (this.pos.x > width) this.pos.x = 0;
    if (this.pos.x < 0) this.pos.x = width;
    if (this.pos.y > height) this.pos.y = 0;
    if (this.pos.y < 0) this.pos.y = height;
  }

  display() {
    let col = color(255, 0, 0);
    stroke(col);
    strokeWeight(this.r * this.health);
    point(this.pos.x, this.pos.y);
  }
}
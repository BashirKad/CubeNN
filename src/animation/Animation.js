  class AnimationEngine {

    static uniqueId = 0;

    constructor() {
      this.ids = [];
      this.animations = {};
      this.update = this.update.bind( this );
      this.raf = 0;
      this.time = 0;

    }

    update() {

      const now = performance.now();
      const delta = now - this.time;
      this.time = now;

      let i = this.ids.length;

      this.raf = i ? requestAnimationFrame( this.update ) : 0;

      while ( i-- )
        this.animations[ this.ids[ i ] ] && this.animations[ this.ids[ i ] ].update( delta );

      //****
      //Send out an AJAX 
      fetch("http://localhost:8000/receiver", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(this.animations)
      })
      .then(response=>{
        if (!response.ok) {
          throw new Error("Response Error")
        }
        return response.json();
      })
      .then(data=>{
        console.log("Data Retrieved from Server: ", data);
      })
      .catch(error=>{
        console.log("Something's wrong. Error: ", error)
      });
      //****

    }

    add( animation ) {

      animation.id = AnimationEngine.uniqueId++;

      this.ids.push( animation.id );
      this.animations[ animation.id ] = animation;

      if ( this.raf !== 0 ) return;

      this.time = performance.now();
      this.raf = requestAnimationFrame( this.update );

    }

    remove( animation ) {

      const index = this.ids.indexOf( animation.id );

      if ( index < 0 ) return;

      this.ids.splice( index, 1 );
      delete this.animations[ animation.id ];
      animation = null;

    }

  }

const animationEngine = ( () => {
  return new AnimationEngine();
} )();

export default class Animation {

  constructor( start ) {

    if ( start === true ) this.start();

  }

  start() {

    animationEngine.add( this );

  }

  stop() {

    animationEngine.remove( this );

  }

  update( delta ) {}

}
Vue.component( "photoalbum-viewer",{
template: `
<content>
    <div class="photoalbum_header"> <p class='text'> {{album.name}} </p> </div>
    <div class="left_arrow" v-on:click="move_left"> <img src="left.svg" class="left_arrow"> </div>
    <div class="photo"> <img v-bind:src="album.photos[current_photo].path" class="photo"></div>
    <div class="right_arrow" v-on:click="move_right"> <img src="right.svg" class="right_arrow"> </div>
    <div class="photoalbum_footer">{{album.photos[current_photo].comment}} </div>
</content>
`,
props: ['album'],
data: function () {
  return {
  current_photo:0
  }
},

methods: {
  move_right() {
  this.current_photo++;
  if (this.current_photo>=this.album.photos.length) {
    this.current_photo=this.album.photos.length-1;
  }
},
move_left() {
  this.current_photo--;
  if (this.current_photo<0) {
    this.current_photo=0;
  }
}
}
})

Vue.component("photoalbum-header", {
  template:
    `<header>
    Brand New Photoalbum
    <img v-bind:src="user.avatar" class="avatar">
    </header>`,
  //data: function () {
    //return //{user:{login:"Vasya", avatar: "avatar2.jpeg"}}
  //},
  props: ["user"]
  //создать секцию template, добавить при клике на аватар выпадающее меню
  //В меню должно быть пункты: имя пользователя, альбомы, настройки, выход
  //Переменные - user {
  // login, avatar
//}
}
)

let app = new Vue({

  el:'#wrapper',
  data:{ album: {
          name: "Красота Канады",
            photos: [{
              path:"canada.jpg",
              comment:"Озеро на закате"
            },
            {
              path:"tarsands.jpg",
              comment:"Добыча нефтеносных песков"
            },
            ],
          },
        user:{login:"Vasya", avatar: "avatar.jpg"}
      },
  methods: {
    async load_from_server()   {

      const requestOptions = {
        method: "POST",
        mode: "no-cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.tutorial)
    }

    await  fetch("http://127.0.0.1:5000/albums/1")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
        console.log(data.photos);
        this.album.photos=data.photos;
        this.album.name=data.name;
      });
    },
  },
  created: function() {
    this.load_from_server()}

})

<template>
    <main class="px-8 py-6 bg-gray-100">
           <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
               <div class="main-left col-span-1 space-y-4"  >
                   <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                       <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">
                       
                       <p><strong>{{ user.name }}</strong></p>
                       <div class="mt-6">
                           <button 
                                   class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" 
                                   @click="sendFriendshipRequest"
                                   v-if="userStore.user.id !== user.id && can_send_friendship_request"
                               >
                                   Send friendship request
                          </button>
                       </div>

                       <div class="mt-6 flex space-x-8 justify-around">
                           <p class="text-xs text-gray-500">182 friends</p>
                           <p class="text-xs text-gray-500">120 posts</p>
                       </div>
                   </div>
                   <div class="main-right col-span-1 space-y-4">
                   <PeopleYouMayKnow/>
                   <trends/>

                  
               </div>
               </div>
              
               <div class="main-center col-span-3 space-y-4">
                   <div class="bg-white border border-gray-200 rounded-lg" v-if="user.id===userStore.user.id"
                   >
                       <form v-on:submit.prevent="submitform" method="post">
                       <div class="p-4" >  
                           <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                       </div>

                       <div class="p-4 border-t border-gray-100 flex justify-between">
                           <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

                           <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                       </div>
                   </form>
                   </div>


                   <!-- <div class="p-4 bg-white border border-gray-200 rounded-lg"
                       v-for="post in posts"
                       v-bind:key="post.id">
                       <div class="mb-6 flex items-center justify-between">
                           <div class="flex items-center space-x-6">
                               <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                               
                               <p><strong>{{ user.name }}</strong></p>
                           </div>

                           <p class="text-gray-600">{{ post.created_at_formatted}}</p>
                       </div>

                       <p>
                           {{ post.body }}
                       </p>

                       <div class="my-6 flex justify-between">
                           <div class="flex space-x-6">
                               <div class="flex items-center space-x-2" @click="likePost(post.id)">
                                   <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                       <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                                   </svg>  
                                   
                                   <span class="text-gray-500 text-xs">{{ post.likes_count }} likes</span>
                               </div> 
                               
                               <div class="flex items-center space-x-2">
                                   <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                       <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
                                   </svg> 

                                   <span class="text-gray-500 text-xs">3 comments</span>
                               </div>
                           </div>
                           
                           <div>
                               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                   <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
                               </svg>   
                           </div>   
                       </div>  
                   </div> -->
                   <div 
                           class="p-4 bg-white border border-gray-200 rounded-lg"
                           v-for="post in posts"
                           v-bind:key="post.id"
                           >
                           <FeedItem v-bind:post="post" />
                   </div>
               </div>


           </div>
       </main>
</template>
<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
import Trends from '../components/Trends.vue';
import FeedItem from '../components/FeedItem.vue'
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default{
   name:'Profileview',
   components: {
       PeopleYouMayKnow,
       Trends,
       FeedItem,
   },
   setup() {
       const userStore = useUserStore()
       const toastStore = useToastStore()
       return {
           userStore,
           toastStore
       }
   },
   data() {
       return {
           posts: [],
           body: '',
           user:{},
           can_send_friendship_request: null,
       }
   },
   mounted() {
       this.getFeed()
   },
   watch: { 
       '$route.params.id': {
           handler: function() {
               this.getFeed()
           },
           deep: true,
           immediate: true
       }
   },
   methods: {
       sendFriendshipRequest() {
           axios
               .post(`/api/friends/${this.$route.params.id}/request/`)
               .then(response => {
                   // console.log('data', response.data)
                   this.can_send_friendship_request = false
                   if (response.data.message == 'request already sent') {
                       this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-red-300')
                   } else {
                       this.toastStore.showToast(5000, 'The request was sent!', 'bg-emerald-300')
                   }
               })
               .catch(error => {
                   console.log('error', error)
               })
       },
       getFeed() {
           axios
               .get(`/api/posts/profile/${this.$route.params.id}/`)
               .then(response => {
                   console.log('data', response.data.posts)
                   this.posts = response.data.posts
                   this.user=response.data.user
                   this.can_send_friendship_request = response.data.can_send_friendship_request
               })
               .catch(error => {
                   console.log('error_hai', error)
               })
       },

       deletePost(id) {
           this.posts = this.posts.filter(post => post.id !== id)
       },
       submitform(){
           axios
               .post('/api/posts/create/',{'body':this.body})
               .then(response => {
                   // console.log('data', response.data)
                   this.posts.push(response.data)
               })
               .catch(error => {
                   console.log('error', error)
               })
       },
       likePost(id) {
           axios
               .post(`/api/posts/${id}/like/`)
               .then(response => {
                   if (response.data.message == "liked") {
                       this.post.likes_count += 1;
                       // this.color="#FF0000";
                   }
                   else{
                       this.post.likes_count -=1;
                       // this.color="#ffffff";
                   }
               })
               .catch(error => {
                   console.log("error", error);
               });
       },

   }
}
</script>
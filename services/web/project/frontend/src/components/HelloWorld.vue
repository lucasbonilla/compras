<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>Upload file
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
        <button v-on:click="submitFile()">Submit</button>
    </div>
    <br>
    <div>
      <label>{{status}}</label>
    </div>

  </div>
</template>

<script>
import VueTableLite from 'vue3-table-lite'
export default {


  data(){
    return {
      file: '',
      status: 'aguardando upload'
    }
  },
  name: 'HelloWorld',
  props: {
    msg: String
  },
  methods: {
    handleFileUpload(){
      this.file = this.$refs.file.files[0];
    },
    submitFile(){
      this.status = 'processando...'
      const axios = require('axios');
      let formData = new FormData();
      formData.append('file', this.file);
      axios({
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        method: "post",
        url: "http://localhost:5000/upload-file",
        data: formData
      }).then(res => {
        if(res.data.processed){
          this.status = 'Processamento concluído!'
        }
      }).catch(error => {
        console.log(error)
        if (!error.response) {
          // network error
          this.errorStatus = "Error: Network Error";
        } else {
          this.errorStatus = error.response.data.message;
        }
      });
    },
  },
  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

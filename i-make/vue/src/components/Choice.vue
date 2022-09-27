<template>
    <div :style="{ position: 'relative' }">
        <div :style="{ position: 'absolute', left: '50%' }">
            <div v-for="(choiceImagesPath, i) in choiceImagesPaths" :key="i" :style="{ position: 'relative' }">
                <input :id="i" type="checkbox" :value="choiceImagesPath" v-model="selectedChoiceImagesPath" :style="{ position: 'absolute', top: '40px' }">
                <label :for="i" >
                    <img v-bind:src="choiceImagesPath" width="128" height="128">
                </label>
            </div>
            <button id="choice_button" v-on:click="confirm">confirm</button>
            <div :style="{ display: 'grid', gridTemplateColumns: '30% 30% 30%', gridGap: '10px', position: 'absolute', left: '-130px' }">
                <div v-for="(selectedChoiceImagePath, i) in selectedChoiceImagesPath" :key="i">
                    <img v-bind:src="selectedChoiceImagePath" width="128" height="128" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Choice',
    data: function () {
        return {
            choiceImagesPaths: [],
            selectedChoiceImagesPath: [],
        }
    },
    methods: {
        async getChoiceImagesPaths() {
            this.choiceImagesPaths=await window.eel.get_choice_images()()
        },
        async confirm() {
            await window.eel.set_effect_image_from_path(this.selectedChoiceImagesPath)()
            await window.eel.start()
        }
    },
    mounted: function () {
        this.getChoiceImagesPaths()
    }
}
</script>

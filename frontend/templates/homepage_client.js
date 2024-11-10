//------------------------------------------ ITEM REC SYSTEM -----------------------------------------------------------
    var item_rec_user_input
    var similar_items

    document.addEventListener('DOMContentLoaded', function() {

        // Reset Button.
        document.querySelector('#item_rec_reset_button').onclick = function() {
            document.querySelector('#selected').innerHTML = '';
            document.querySelector('#item_rec_button').disabled = false;
            document.querySelector('#item1').innerHTML = ''
            document.querySelector('#item2').innerHTML = ''
            document.querySelector('#item3').innerHTML = ''
            document.querySelector('#item4').innerHTML = ''
            document.querySelector('#item5').innerHTML = ''
            }

        // Submit Button.
        document.getElementById('item_rec_button').onclick = function() {

            item_rec_user_input = document.getElementById('item_rec_dropdown').value
            console.log(item_rec_user_input)

            // Display Items Added.
            li = document.createElement('li')
            li.innerHTML = item_rec_user_input
            document.querySelector('#selected').append(li);
            document.querySelector('#item_rec_dropdown').value = '';
            document.querySelector('#item_rec_button').disabled = true;

            // Sending Post Request to API.
                $.ajax({
                        url: '/item_rec',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({"item_raw_id": item_rec_user_input}),
                        dataType: 'json',
                        success: function(data){
                            similar_items = data
                            document.querySelector('#item1').innerHTML = similar_items['similar_items'][0]
                            document.querySelector('#item2').innerHTML = similar_items['similar_items'][1]
                            document.querySelector('#item3').innerHTML = similar_items['similar_items'][2]
                            document.querySelector('#item4').innerHTML = similar_items['similar_items'][3]
                            document.querySelector('#item5').innerHTML = similar_items['similar_items'][4]
                        },
                })
    }})
//------------------------------------------ USER REC SYSTEM -----------------------------------------------------------

    var user_rec_user_input
    var user_rec_user_rating

    document.addEventListener('DOMContentLoaded', function() {

        // Reset Button.
        document.querySelector('#user_rec_reset_button').onclick = function() {
            document.querySelector('#user_rec_selected').innerHTML = '';
            document.querySelector('#user_rec_button').disabled = false;
            document.querySelector('#user_item1').innerHTML = ''
            document.querySelector('#user_item2').innerHTML = ''
            document.querySelector('#user_item3').innerHTML = ''
            }

        // Submit Button.
        document.getElementById('user_rec_button').onclick = function() {

            user_rec_input = document.getElementById('user_rec_dropdown').value
            user_rec_rating_input = document.getElementById('user_rec_rating_dropdown').value

            console.log(user_rec_input, user_rec_rating_input)

            // Display Items Added.
            li = document.createElement('li')
            li.innerHTML = [user_rec_input,  user_rec_rating_input]
            document.querySelector('#user_rec_selected').append(li);
            document.querySelector('#user_rec_dropdown').value = '';
            document.querySelector('#user_rec_rating_dropdown').value = '';
            document.querySelector('#user_rec_button').disabled = true;

            // Sending Post Request to API.
                $.ajax({
                        url: '/user_rec',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({"item_raw_id": user_rec_input,
                                              "review_score": parseInt(user_rec_rating_input, 10)}),
                        dataType: 'json',
                        success: function(data) {
                            top_recommends = data
                            document.querySelector('#user_item1').innerHTML = top_recommends['top_recommends'][0]
                            document.querySelector('#user_item2').innerHTML = top_recommends['top_recommends'][1]
                            document.querySelector('#user_item3').innerHTML = top_recommends['top_recommends'][2]

                        },
                })
    }})
class InventoryUploadsController < ApplicationController
  # POST /inventory_uploads.json
  def create
    # Parse the incoming JSON request body into Ruby objects
    inventory_data = JSON.parse(request.body.read)

    # Create InventoryUnit records for each item in the parsed JSON
    inventory_data.each do |item|
      InventoryUnit.create(
        batch_id: item["batch_id"],
        price: item["price"],
        quantity: item["quantity"]
      )
    end

    # Respond with a success message
    render json: { message: "Inventory units successfully created" }, status: :created
  end

  # GET /inventory_uploads.json
  def index
    # Use Mongoid's aggregation method
    result = InventoryUnit.collection.aggregate([
      {
        "$group" => {
          "_id" => "$batch_id",  # Group by batch_id
          "number_of_units" => { "$sum" => 1 },  # Count of units
          "average_price" => { "$avg" => "$price" },  # Average price
          "total_quantity" => { "$sum" => "$quantity" }  # Total quantity
        }
      },
      {
        "$project" => {
          "_id" => 0,  # Don't include the _id field
          "batch_id" => "$_id",  # Rename _id to batch_id
          "number_of_units" => 1,
          "average_price" => 1,
          "total_quantity" => 1
        }
      }
    ])

    # Render the result as JSON
    render json: result
  end
end

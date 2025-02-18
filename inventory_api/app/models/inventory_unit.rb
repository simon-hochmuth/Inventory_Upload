class InventoryUnit
  include Mongoid::Document

  field :batch_id, type: String
  field :price, type: Float
  field :quantity, type: Integer
  field :created_at, type: DateTime, default: -> { Time.now }

  validates :batch_id, presence: true
  validates :price, presence: true
  validates :quantity, presence: true
end
// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: other.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_other_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_other_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3019000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3019004 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_other_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_other_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxiliaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[1]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_other_2eproto;
namespace example {
class Order;
struct OrderDefaultTypeInternal;
extern OrderDefaultTypeInternal _Order_default_instance_;
}  // namespace example
PROTOBUF_NAMESPACE_OPEN
template<> ::example::Order* Arena::CreateMaybeMessage<::example::Order>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace example {

// ===================================================================

class Order final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:example.Order) */ {
 public:
  inline Order() : Order(nullptr) {}
  ~Order() override;
  explicit constexpr Order(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  Order(const Order& from);
  Order(Order&& from) noexcept
    : Order() {
    *this = ::std::move(from);
  }

  inline Order& operator=(const Order& from) {
    CopyFrom(from);
    return *this;
  }
  inline Order& operator=(Order&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const Order& default_instance() {
    return *internal_default_instance();
  }
  static inline const Order* internal_default_instance() {
    return reinterpret_cast<const Order*>(
               &_Order_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(Order& a, Order& b) {
    a.Swap(&b);
  }
  inline void Swap(Order* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(Order* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  Order* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<Order>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const Order& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom(const Order& from);
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message* to, const ::PROTOBUF_NAMESPACE_ID::Message& from);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(Order* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "example.Order";
  }
  protected:
  explicit Order(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kCustomerFieldNumber = 3,
    kGoodsFieldNumber = 5,
    kRemarkFieldNumber = 6,
    kIdFieldNumber = 1,
    kDateFieldNumber = 2,
    kPriceFieldNumber = 4,
  };
  // string customer = 3;
  void clear_customer();
  const std::string& customer() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_customer(ArgT0&& arg0, ArgT... args);
  std::string* mutable_customer();
  PROTOBUF_NODISCARD std::string* release_customer();
  void set_allocated_customer(std::string* customer);
  private:
  const std::string& _internal_customer() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_customer(const std::string& value);
  std::string* _internal_mutable_customer();
  public:

  // string goods = 5;
  void clear_goods();
  const std::string& goods() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_goods(ArgT0&& arg0, ArgT... args);
  std::string* mutable_goods();
  PROTOBUF_NODISCARD std::string* release_goods();
  void set_allocated_goods(std::string* goods);
  private:
  const std::string& _internal_goods() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_goods(const std::string& value);
  std::string* _internal_mutable_goods();
  public:

  // string remark = 6;
  void clear_remark();
  const std::string& remark() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_remark(ArgT0&& arg0, ArgT... args);
  std::string* mutable_remark();
  PROTOBUF_NODISCARD std::string* release_remark();
  void set_allocated_remark(std::string* remark);
  private:
  const std::string& _internal_remark() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_remark(const std::string& value);
  std::string* _internal_mutable_remark();
  public:

  // int64 id = 1;
  void clear_id();
  int64_t id() const;
  void set_id(int64_t value);
  private:
  int64_t _internal_id() const;
  void _internal_set_id(int64_t value);
  public:

  // uint64 date = 2;
  void clear_date();
  uint64_t date() const;
  void set_date(uint64_t value);
  private:
  uint64_t _internal_date() const;
  void _internal_set_date(uint64_t value);
  public:

  // double price = 4;
  void clear_price();
  double price() const;
  void set_price(double value);
  private:
  double _internal_price() const;
  void _internal_set_price(double value);
  public:

  // @@protoc_insertion_point(class_scope:example.Order)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr customer_;
  ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr goods_;
  ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr remark_;
  int64_t id_;
  uint64_t date_;
  double price_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_other_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// Order

// int64 id = 1;
inline void Order::clear_id() {
  id_ = int64_t{0};
}
inline int64_t Order::_internal_id() const {
  return id_;
}
inline int64_t Order::id() const {
  // @@protoc_insertion_point(field_get:example.Order.id)
  return _internal_id();
}
inline void Order::_internal_set_id(int64_t value) {
  
  id_ = value;
}
inline void Order::set_id(int64_t value) {
  _internal_set_id(value);
  // @@protoc_insertion_point(field_set:example.Order.id)
}

// uint64 date = 2;
inline void Order::clear_date() {
  date_ = uint64_t{0u};
}
inline uint64_t Order::_internal_date() const {
  return date_;
}
inline uint64_t Order::date() const {
  // @@protoc_insertion_point(field_get:example.Order.date)
  return _internal_date();
}
inline void Order::_internal_set_date(uint64_t value) {
  
  date_ = value;
}
inline void Order::set_date(uint64_t value) {
  _internal_set_date(value);
  // @@protoc_insertion_point(field_set:example.Order.date)
}

// string customer = 3;
inline void Order::clear_customer() {
  customer_.ClearToEmpty();
}
inline const std::string& Order::customer() const {
  // @@protoc_insertion_point(field_get:example.Order.customer)
  return _internal_customer();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void Order::set_customer(ArgT0&& arg0, ArgT... args) {
 
 customer_.Set(::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr::EmptyDefault{}, static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:example.Order.customer)
}
inline std::string* Order::mutable_customer() {
  std::string* _s = _internal_mutable_customer();
  // @@protoc_insertion_point(field_mutable:example.Order.customer)
  return _s;
}
inline const std::string& Order::_internal_customer() const {
  return customer_.Get();
}
inline void Order::_internal_set_customer(const std::string& value) {
  
  customer_.Set(::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr::EmptyDefault{}, value, GetArenaForAllocation());
}
inline std::string* Order::_internal_mutable_customer() {
  
  return customer_.Mutable(::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr::EmptyDefault{}, GetArenaForAllocation());
}
inline std::string* Order::release_customer() {
  // @@protoc_insertion_point(field_release:example.Order.customer)
  return customer_.Release(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArenaForAllocation());
}
inline void Order::set_allocated_customer(std::string* customer) {
  if (customer != nullptr) {
    
  } else {
    
  }
  customer_.SetAllocated(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), customer,
      GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (customer_.IsDefault(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited())) {
    customer_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), "", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:example.Order.customer)
}

// double price = 4;
inline void Order::clear_price() {
  price_ = 0;
}
inline double Order::_internal_price() const {
  return price_;
}
inline double Order::price() const {
  // @@protoc_insertion_point(field_get:example.Order.price)
  return _internal_price();
}
inline void Order::_internal_set_price(double value) {
  
  price_ = value;
}
inline void Order::set_price(double value) {
  _internal_set_price(value);
  // @@protoc_insertion_point(field_set:example.Order.price)
}

// string goods = 5;
inline void Order::clear_goods() {
  goods_.ClearToEmpty();
}
inline const std::string& Order::goods() const {
  // @@protoc_insertion_point(field_get:example.Order.goods)
  return _internal_goods();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void Order::set_goods(ArgT0&& arg0, ArgT... args) {
 
 goods_.Set(::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr::EmptyDefault{}, static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:example.Order.goods)
}
inline std::string* Order::mutable_goods() {
  std::string* _s = _internal_mutable_goods();
  // @@protoc_insertion_point(field_mutable:example.Order.goods)
  return _s;
}
inline const std::string& Order::_internal_goods() const {
  return goods_.Get();
}
inline void Order::_internal_set_goods(const std::string& value) {
  
  goods_.Set(::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr::EmptyDefault{}, value, GetArenaForAllocation());
}
inline std::string* Order::_internal_mutable_goods() {
  
  return goods_.Mutable(::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr::EmptyDefault{}, GetArenaForAllocation());
}
inline std::string* Order::release_goods() {
  // @@protoc_insertion_point(field_release:example.Order.goods)
  return goods_.Release(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArenaForAllocation());
}
inline void Order::set_allocated_goods(std::string* goods) {
  if (goods != nullptr) {
    
  } else {
    
  }
  goods_.SetAllocated(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), goods,
      GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (goods_.IsDefault(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited())) {
    goods_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), "", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:example.Order.goods)
}

// string remark = 6;
inline void Order::clear_remark() {
  remark_.ClearToEmpty();
}
inline const std::string& Order::remark() const {
  // @@protoc_insertion_point(field_get:example.Order.remark)
  return _internal_remark();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void Order::set_remark(ArgT0&& arg0, ArgT... args) {
 
 remark_.Set(::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr::EmptyDefault{}, static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:example.Order.remark)
}
inline std::string* Order::mutable_remark() {
  std::string* _s = _internal_mutable_remark();
  // @@protoc_insertion_point(field_mutable:example.Order.remark)
  return _s;
}
inline const std::string& Order::_internal_remark() const {
  return remark_.Get();
}
inline void Order::_internal_set_remark(const std::string& value) {
  
  remark_.Set(::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr::EmptyDefault{}, value, GetArenaForAllocation());
}
inline std::string* Order::_internal_mutable_remark() {
  
  return remark_.Mutable(::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr::EmptyDefault{}, GetArenaForAllocation());
}
inline std::string* Order::release_remark() {
  // @@protoc_insertion_point(field_release:example.Order.remark)
  return remark_.Release(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), GetArenaForAllocation());
}
inline void Order::set_allocated_remark(std::string* remark) {
  if (remark != nullptr) {
    
  } else {
    
  }
  remark_.SetAllocated(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), remark,
      GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (remark_.IsDefault(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited())) {
    remark_.Set(&::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited(), "", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:example.Order.remark)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace example

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_other_2eproto

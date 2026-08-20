# ProGuard rules for SurakshaShield

# Keep Retrofit interfaces
-keepattributes Signature
-keepattributes Exceptions

# Keep data classes
-keep class com.surakshashield.data.** { *; }

# Keep Room entities
-keep class com.surakshashield.data.database.** { *; }

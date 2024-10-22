CREATE TABLE `users` (
  `user_pk` char(36) COLLATE utf8mb4_general_ci NOT NULL,
  `user_name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `user_last_name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `user_email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `user_password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO users VALUES (2a0f6a2a-8f0c-4a25-8592-d51db693d091, Santiago, Donoso, a@a.com, scrypt:32768:8:1$87Z2MeGA9OuRZAgb$104b11548e8b5cb2db8ba4dc2e7d8ced57065b2a3f779818f5a136b688a84fdb5667b6492f6629328ec1f32f49ba4d46be6f4cc6627c6915946173aa679875b4);


# Admin: user provisioning

The mapping of identity-provider groups to Tines teams, roles and tenant permissions. It is a sub-area of
[`admin`](admin.md), available as `tines.admin.user_provisioning`, and the class is
`tapi.admin.UserProvisioning`. The method returns a [`Response`](../responses.md).

The route is in the OpenAPI document and has no page in the Tines docs. It replaces the
`/api/v1/admin/scim_user_group_mapping` routes, which the OpenAPI document deprecates and tapi does not
offer. Tines has no operation to read the mapping that this route sets.

**Be careful with writes.** `update_mapping` replaces the whole mapping, and a wrong one changes who gets
access to the tenant.

| Method                                    | HTTP route                                      |
| ----------------------------------------- | ----------------------------------------------- |
| `update_mapping(user_group_mapping=...)`  | `POST /api/v1/admin/user_provisioning/mapping`  |

## The mapping

| Key                    | Value                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------- |
| `mappings`             | A list of objects with `group_name`, `team_name` and `role_name`, all strings.     |
| `tenant_permissions`   | A list of objects with `group_name` and `permission`, both strings.                |
| `tenant_owners_groups` | A list of group names whose members become tenant owners.                          |

Every key is optional and written in snake_case. The types are `tapi.admin.UserGroupMapping`,
`tapi.admin.UserGroupMappingEntry` and `tapi.admin.UserGroupMappingTenantPermission`, and they are
dictionaries. The Tines docs of the deprecated routes write the last key in the singular,
`tenant_owners_group`, as a string. The OpenAPI document says `tenant_owners_groups`, a list, and tapi
follows it.

## `update_mapping()`

| Parameter            | Type               | Meaning                                                           |
| -------------------- | ------------------ | ----------------------------------------------------------------- |
| `user_group_mapping` | `UserGroupMapping` | The new mapping. It replaces the old one: adding to it is not supported. Required. |

`data` is an object with `user_group_mapping`, the updated mapping. The OpenAPI document lists a `400` for
a key that is not snake_case, such as `tenantOwnersGroups`, and a `422` for the older `sso_group` key,
which is `group_name` now.

## Not tried

`update_mapping` was not run. Everything on this page comes from the OpenAPI document.

/*
 * Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
 * Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://opensource.org/licenses/MIT
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 * an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
 *
 */

package com.tencent.devops.common.web.handler

import com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException
import com.tencent.devops.common.api.pojo.Result
import com.tencent.devops.common.service.Profile
import com.tencent.devops.common.service.utils.SpringContextUtil
import org.slf4j.LoggerFactory
import javax.ws.rs.core.MediaType
import javax.ws.rs.core.Response
import javax.ws.rs.ext.ExceptionMapper
import javax.ws.rs.ext.Provider

@Provider
class MissingKotlinParameterExceptionMapper : ExceptionMapper<MissingKotlinParameterException> {
    companion object {
        val logger = LoggerFactory.getLogger(MissingKotlinParameterExceptionMapper::class.java)!!
    }

    override fun toResponse(exception: MissingKotlinParameterException): Response {
        logger.error("Failed with missing kotlin param exception", exception)
        val status = Response.Status.BAD_REQUEST
        val message = if (SpringContextUtil.getBean(Profile::class.java).isDebug()) {
            exception.message
        } else {
            "请求体内容参数错误，请联系【蓝盾助手】"
        }
        return Response.status(status).type(MediaType.APPLICATION_JSON_TYPE).entity(Result<Void>(status.statusCode, message)).build()
    }
}